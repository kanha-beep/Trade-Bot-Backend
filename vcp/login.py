import requests

BASE_URL = "https://ant.aliceblueonline.com"

def alice_login():
    """Attempt Alice Blue login - returns None if fails"""
    try:
        login_url = f"{BASE_URL}/rest/AliceBlueAPIService/api/customer/getUserSID"
        
        payload = {
            "userid": "1044414",
            "password": "Taking@2021",
            "twoFA": "20040123",
            "vendor_code": "1044414",
            "api_secret": "mKDhVLgSITTD29mMN6hC2AKv98VhTSOKdoAmnWhpH4hi5NSlE3fmvcYqxPFdGHg3kxdqHX0gjmsLN2jGjBrXJLV5rc0LUl5pBGK9qaEcizN0T1y6AUBHHu2T4rmy2bCV"
        }
        
        response = requests.post(login_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("stat") == "Ok":
                return data.get("susertoken")
        
        print(f"Alice Blue API failed: Status {response.status_code}")
        return None
        
    except Exception as e:
        print(f"Alice Blue login error: {e}")
        return None

# For now, just return None since API is not working
def get_access_token():
    """Get Alice Blue access token or None if unavailable"""
    return alice_login()

if __name__ == "__main__":
    token = get_access_token()
    if token:
        print("Access Token:", token)
    else:
        print("Alice Blue API unavailable - using fallback mode")
