#ifndef _EC_POINT__H__
#define _EC_POINT__H__

#include <DYNAMIC_LIBRARY_API.hpp>

#ifdef EXPORT_ECPoints
#    define ECPoint_API EXPORT_DYNAMIC_LIBRARY
#else
#    define ECPoint_API IMPORT_DYNAMIC_LIBRARY
#endif

#include <memory>
#include <string>
#include <ECPoint/ECPointImpl.h>

class ECPointImpl; 

class ECPoint_API ECPoint
{
    friend ECPoint ECPoint_API operator+ (const ECPoint&, const ECPoint&);
    friend bool ECPoint_API operator == (const ECPoint&, const ECPoint&);
    friend bool ECPoint_API operator != (const ECPoint&, const ECPoint&);

    public:
        explicit ECPoint();
        ~ECPoint();
        ECPoint(const int& nid);

        //moveable
        ECPoint(ECPoint&& obj) noexcept;
        ECPoint& operator=(ECPoint&& obj) noexcept;

        //copyable
        ECPoint(const ECPoint& obj);
        ECPoint& operator=(const ECPoint& obj);

        ECPoint MulHex(const std::string& objm, const std::string& objn);
        ECPoint MulDec(const std::string& objm, const std::string& objn);
        ECPoint Double();
        void Invert();
        bool CheckInfinity();
        bool CheckOnCurve();
        static CurveList getCurveList();
        std::string ToHex();
        int GroupNid()const;
        bool FromHex(const std::string& hexStr, int nid);

    private:
        const ECPointImpl* pImpl() const { return m_pImpl.get(); }
        ECPointImpl* pImpl() {return m_pImpl.get();}       

        std::unique_ptr<ECPointImpl> m_pImpl ; 
};

#endif //ifndef _EC_POINT__H__


