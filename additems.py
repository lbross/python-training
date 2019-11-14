#  Name: addItem.py
#
#
#  Purpose: adds image items and shares publicly. This is a sample written in
#           2.7. more current supportable sample can be found here:
# https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html?highlight=add%20item#arcgis.gis.ContentManager
# https://developers.arcgis.com/python/sample-notebooks/publishing-sd-shapefiles-and-csv/#Publish-all-the-service-definition-files-in-a-folder

#
# Author:      Kelly Gerrow
#Contact:      kgerrow@esri.com
#
# Created:     10/3/2016
#-------------------------------------------------------------------------------

import os, sys, string, requests,json, time
import fnmatch, fileinput

# Create Token based on username and password
def getToken(adminUser, pw):
        data = {'username': adminUser,
            'password': pw,
            'referer' : 'https://www.arcgis.com',
            'f': 'json'}
        url  = 'https://arcgis.com/sharing/rest/generateToken'
        jres = requests.post(url, data=data, verify=False).json()
        return jres['token'], jres['ssl']


#Get account information and return the URLkey
def GetAccount(token, pref):
        URL= pref+'www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
        response = requests.get(URL, verify=False)
        jres = json.loads(response.text)
        return jres['urlKey']




if __name__ == "__main__":
    #Directory containing the Error Reports to process
    textdir = r"C:\test1"
#enter username and password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    tok = getToken(user,pw)
    token = tok[0]
    ssl=tok[1]
    #construct short URl with correct protocol
    if ssl == False:
        pref='http://'
    else:
        pref='https://'

    urlKey= GetAccount(token, pref)
    portalUrl = pref+urlKey




#loop through files in directory
    for root, dirs, filenames in os.walk(textdir):
        for f in filenames:

        #upload URL
         uploadPartURL ='{}.maps.arcgis.com/sharing/rest/content/users/{}/addItem'.format(portalUrl, user)
         #file path
         inputTextFile = os.path.abspath(os.path.join(root, f))
         filesUp = {"file": open(inputTextFile, 'rb')}
         #add URL parameters
         url = uploadPartURL + "?f=json&token="+token+ \
                    "&async=" + "True"+\
                    "&type="+"Image"+\
                    "&title="+ f+ \
                    "&tags="+"test"+\
                    "&description="+"This is an upload test"
         #submit post request
         response = requests.post(url, files=filesUp)
         #check for resulting item ID
         destItemID= json.loads(response.text)['id']
         time.sleep(2)


         shareurl = '{}.maps.arcgis.com/sharing/rest/content/users/{}/shareItems'.format(portalUrl, user)
         data ={'everyone': 'true', 'account': 'true', 'items':destItemID, 'f':'json', 'token':token}
         jres = requests.post(shareurl, data=data, verify=False).json()
         print jres


         filesUp['file'].close()





