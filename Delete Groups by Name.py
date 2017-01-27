# imports for the Duo AdminAPI calls
import duo_client

# We use time to create a faux limiter for making API calls
import time

# Constants for Duo API calls
DUO_IKEY = "xxxxxxxxxxxxxxxxxxxxxx"
DUO_SKEY = "xxxxxxxxxxxxxxxxxxxxxx"
DUO_APIHOSTNAME = "xxxxxxxxxxxxxxxxxxxxxx"

# we will be using this to check for the word in group names
SEARCH_STRING = 'with'

# Print out timestamp information in case we are logging this
print "=============================="
print time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
print "=============================="

# authorization information for Duo API call
duoAPI = duo_client.Admin(
    ikey=DUO_IKEY,
    skey=DUO_SKEY,
    host=DUO_APIHOSTNAME
)

#Get list of groups from Duo
duoGroups = duoAPI.get_groups()

# build dictionary of groupname -> group_id
duoGroupList = {}

for group in duoGroups:
    if group['name'] not in duoGroupList:
        duoGroupList[group['name']] = group['group_id']

# identify groups with test in groupname
groupListToDelete = [ duoGroupList[group_name] for group_name in duoGroupList.keys() if SEARCH_STRING in group_name ]

print groupListToDelete

# now that we have the list of groups to delete start calling delete_group()
for group in groupListToDelete:
    duoAPI.delete_group(group)
    print "Deleted group with ID: " + str(group)
    # add in a .3 second delay between calls to prevent getting errors
    time.sleep(0.3)
