#################################################################
#  Date             24/04/2019                                  #
#  Author           nChain's employees                          #
#                                                               #
#  Copyright (c) 2019 nChain Limited. All rights reserved       #
#################################################################

if(NOT Boost_FOUND)
  message(STATUS "SDK WARNS : Boost was not found on your system, unit tests will not be built")
  return()
endif()

macro(sdk_add_unit_test _targetName)
  if(NOT TARGET ${_targetName})
      message(FATAL_ERROR " [${_targetName}] is not a TARGET")
  endif()
  sdkLinkTargetToBoost(${_targetName} Boost::unit_test_framework)

  if(CMAKE_CONFIGURATION_TYPES)
    set(_tpost_fix ${CMAKE_DEBUG_POSTFIX})
    ## Note at the moment, on Windows Py Module can be loaded only in release build. There are problem in debug build
    add_test(NAME ${_targetName} COMMAND $<TARGET_FILE:${_targetName}> --report_format=HRF --report_level=detailed --log_format=JUNIT --log_sink=$<TARGET_FILE:${_targetName}>.xml CONFIGURATIONS Release)
    add_test(NAME ${_targetName}${_tpost_fix} COMMAND $<TARGET_FILE:${_targetName}> --report_format=HRF --report_level=detailed --log_format=JUNIT --log_sink=$<TARGET_FILE:${_targetName}>.xml CONFIGURATIONS Debug)
  else()
    if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
      set(_tpost_fix ${CMAKE_DEBUG_POSTFIX})
    endif()
    add_test(NAME ${_targetName}${_tpost_fix} COMMAND $<TARGET_FILE:${_targetName}> --report_format=HRF --report_level=detailed --log_format=JUNIT --log_sink=$<TARGET_FILE:${_targetName}>.xml)
  endif()
endmacro()

add_executable(test_BigNumbers test_BigNumbers.cpp test_BigNumbersRandom.cpp)
target_link_libraries(test_BigNumbers BigNumbers)
set_target_properties(test_BigNumbers PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_BigNumbers)

add_executable(test_MessageHash test_MessageHash.cpp)
target_link_libraries(test_MessageHash MessageHash BigNumbers) # Might use BigNumbers to generate random string
set_target_properties(test_MessageHash PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_MessageHash)

add_executable(test_Polynomial test_Polynomial.cpp)
target_link_libraries(test_Polynomial BigNumbers Polynomial)
set_target_properties(test_Polynomial PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_Polynomial)

add_executable(test_SecretSplit test_secretsplit.cpp)
target_link_libraries(test_SecretSplit  BigNumbers Polynomial MessageHash SecretSplit)
set_target_properties(test_SecretSplit PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_SecretSplit)

add_executable(test_ECPoint test_ECPoints.cpp)
target_link_libraries(test_ECPoint ECPoint BigNumbers)
set_target_properties(test_ECPoint PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_ECPoint)

add_executable(test_AsymKey test_AsymKey.cpp)
target_link_libraries(test_AsymKey AsymKey BigNumbers ECPoint)
set_target_properties(test_AsymKey PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_AsymKey)

add_executable(test_SymEncDec test_SymEncDec.cpp)
target_link_libraries(test_SymEncDec SymEncDec BigNumbers)# Might use BigNumbers to generate random string
set_target_properties(test_SymEncDec PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
sdk_add_unit_test(test_SymEncDec)

#add_executable(test_GroupPlayers test_GroupPlayer.cpp)
#target_link_libraries(test_GroupPlayers ThresholdSignatures BigNumbers MessageHash ${CMAKE_DL_LIBS} ${CMAKE_THREAD_LIBS_INIT})
#set_target_properties(test_GroupPlayers PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
#sdk_add_unit_test(test_GroupPlayers)

#add_executable(test_GroupBuilder test_GroupBuilder.cpp utils/FuncUtils.cpp)
#set_target_properties(test_GroupBuilder PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
#target_link_libraries(test_GroupBuilder ThresholdSignatures )
#sdk_add_unit_test(test_GroupBuilder)

add_executable(test_BSVAddress test_BSVAddress.cpp)
set_target_properties(test_BSVAddress PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
target_link_libraries(test_BSVAddress AsymKey BSVAddress)
sdk_add_unit_test(test_BSVAddress)

if (WIN32)
	message("Testing TS Protobuf disabled for Windows")
	return()
endif()

add_executable(test_TS_playerAndGroup test_TS_playerAndGroup.cpp)
set_target_properties(test_TS_playerAndGroup PROPERTIES  FOLDER "tests/unit" DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})
target_link_libraries(test_TS_playerAndGroup TSCore BigNumbers ECPoint)
sdk_add_unit_test(test_TS_playerAndGroup)


#########################################################################
## Test case for Protobuf
add_subdirectory(proto)
#########################################################################
