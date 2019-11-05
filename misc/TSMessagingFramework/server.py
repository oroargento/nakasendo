
from twisted.spread import pb
from twisted.internet import reactor

from orchestrator import Orchestrator

#-----------------------------------------------------------------
# Error class 
class OrchestratorError(pb.Error):
    """This is an Expected Exception. Something bad happened."""
    pass

#-----------------------------------------------------------------
# Exception class 
class OrchestraterException(Exception):
    """This is an Unexpected Exception. Something really bad happened."""
    pass

#-----------------------------------------------------------------
# Orchestrator Protocol 
# Contains functionality for transmitting and receiving data,
# using Twisted libaray (See Twisted Perspective Broker for more information) 
class OrchestratorProtocol( pb.Root ) :

    #-------------------------------------------------
    def __init__ (self) :
        print("Server Running...")
        self.orchestrator = Orchestrator( )


    #-------------------------------------------------
    # Register user with Orchestrator
    def remote_register(self, username, ref):
        self.orchestrator.register( username, ref )


    #-------------------------------------------------
    def remote_createGroup(self, proposer, m, n):
        try :
            results =  self.orchestrator.createGroup(proposer, m, n)
        except Exception as inst:
            raise OrchestratorError( inst.args )

        groupId = results[0]
        inviteList = results[1]

        for invitee in inviteList :
            invitee.callRemote("invite", groupId).addCallback \
                    (self.acceptInvite)

        return groupId 

    #-------------------------------------------------
    def acceptInvite(self, data ) :
        
        user        = data[0]
        groupID     = data[1]
        acceptance  = data[2]    

        if self.orchestrator.acceptInvite(user, groupID, acceptance) :
            self.groupIsSet(groupID)

    #-------------------------------------------------
    def groupIsSet(self, groupID):        

        # send message to all users who are part of this group 
        participants = self.orchestrator.getParticipants(groupID)
        for user in participants :
            params = self.orchestrator.getGroupIsSetParameters( user, groupID )

            print ('sending groupIsSet message to {0}'.format(user))
            
            self.orchestrator.getUserRef(user).callRemote \
                ( "groupIsSet", groupID.encode(), params[0], params[1], params[2] ) 
        return

    #-------------------------------------------------
    # This sends a request for data to all participants of group
    def remote_sharePublicKey( self, user, groupId ) :
        groupId = groupId.decode()

        if not self.orchestrator.validGroup(groupId) :
            errMsg = 'Group Id is not valid: {0}'.format(groupId)
            raise OrchestratorError( errMsg )

        participants = self.orchestrator.getParticipants(groupId)

        if user not in participants :
            errMsg = 'user is not in the group: {0}'.format(user)
            raise OrchestratorError( errMsg ) 
        
        userRefs = self.orchestrator.getUserReferences(groupId)
        for ref in userRefs :
            ref.callRemote("requestData", groupId).addCallback \
                (self.collateEncryptedCoeffs)        
        return

    #-------------------------------------------------
    # collate data
    def collateEncryptedCoeffs(self,  data ) :

        groupId     = data[0]
        ordinal     = data[1]
        evals       = data[2] 
        hiddenPoly  = data[3]
        hiddenEvals = data[4]

        # if True then ready to distribute data
        if self.orchestrator.collateData( groupId, ordinal, evals, hiddenPoly, hiddenEvals) :
            collatedData = self.orchestrator.getCollatedData(groupId) 
            
            # send the public data out to all group participants
            userRefs = self.orchestrator.getUserReferences( groupId )
            for ref in userRefs :
                ref.callRemote( "calculatePrivateKeyShare", groupId, collatedData[0], collatedData[1], collatedData[2]) \
                        .addCallbacks(self.secretVerification)

    #-------------------------------------------------
    # This is here as a placeholder
    def secretVerification(self, data):

        user        = data[0]
        groupId     = data[1]
        ordinal     = data[2]
        msg         = data[3]

        if self.orchestrator.secretVerification(user, groupId, ordinal, msg) :
            print("secretVerification complete")
        

    def groupError(self, message):
        print ("Error: {0}".format(message))
        # do some stuff, delete the group / mark as being errored
        # tell clients this group is not good



#-----------------------------------------------------------------

if __name__ == '__main__':

    reactor.listenTCP(8790, pb.PBServerFactory(OrchestratorProtocol()))
    reactor.run()


