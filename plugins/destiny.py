import requests
import json

from cloudbot import hook

classTypeName = {0: "Titan", 1: "Hunter", 2: "Warlock", 3:''}

@hook.on_start()
def load_api(bot):
    api_key = bot.config.get("api_keys", {}).get("destiny", None)
    HEADERS = {"X-API-Key":api_key}

@hook.command('item')
def item_search(text, bot):
    """ Expects the tex to be a valid object in the Destiny database
       Returns the item's name and description.
       TODO: Implement error checking
   """
    api_key = bot.config.get("api_keys", {}).get("destiny", None)
    HEADERS = {"X-API-Key":api_key}
 
    item = text.strip()
    itemquery = 'https://www.bungie.net/platform/Destiny/Explorer/Items?name=' + item
    itemHash = requests.get(
        itemquery, headers=HEADERS).json()['Response']['data']['itemHashes'];
 
    output = []
    for item in itemHash:        
        itemquery = 'https://www.bungie.net/platform/Destiny/Manifest/inventoryItem/' + str(item)
        result = requests.get(
            itemquery, headers=HEADERS).json()['Response']['data']['inventoryItem'];
 
        output.append('\x02{} \x02({} {} {}) - \x1D{}\x1D - http://www.destinydb.com/items/{}'.format(
            result['itemName'],
            result['tierTypeName'],
            result['classType'],
            result['itemTypeName'],
            result['itemDescription'],
            result['itemHash']
        ))
    return output[:3]
    
@hook.command('nightfall')
def nightfall(bot):
    HEADERS = {"X-API-Key": bot.config.get("api_keys", {}).get("destiny", None)}
 
    result = requests.get(
        'https://www.bungie.net/platform/destiny/advisors/?definitions=true',
        headers=HEADERS).json()
    nightfallActivityId = str(result['Response']['data']['nightfallActivityHash'])
 
    result = requests.get(
        'https://www.bungie.net/platform/destiny/manifest/activity/{}/?definitions=true'
        .format(nightfallActivityId),
        headers=HEADERS).json()
    nightfallDefinition = result.json()['Response']['data']['activity']
 
    if len(nightfallDefinition['skulls']) == 5:
        return '{} - {} | Modifiers: {}, {}, {}'.format(
            nightfallDefinition['activityName'],
            nightfallDefinition['activityDescription'],
            nightfallDefinition['skulls'][1]['displayName'],
            nightfallDefinition['skulls'][2]['displayName'],
            nightfallDefinition['skulls'][3]['displayName']
        )
    else:
        return 'weylin lied to me, get good scrub.'

@hook.command('weekly')
def weekly(bot):
    api_key = bot.config.get("api_keys", {}).get("destiny", None)

    HEADERS = {"X-API-Key":api_key}

    r = requests.get("https://www.bungie.net/platform/destiny/advisors/?definitions=true", headers=HEADERS);

    weeklyHeroicActivityHash = r.json()

    weeklyHeroicId = str(weeklyHeroicActivityHash['Response']['data']['heroicStrike']['activityBundleHash'])

    r = requests.get("https://www.bungie.net/platform/destiny/manifest/activity/" + weeklyHeroicId + "/?definitions=true", headers=HEADERS);

    weeklyHeroicDefinition = r.json()

    weeklyHeroicModifierArrayLength = len(weeklyHeroicDefinition['Response']['data']['activity']['skulls'])

    if weeklyHeroicModifierArrayLength == 2:
        return weeklyHeroicDefinition['Response']['data']['activity']['activityName'] + ' - ' + weeklyHeroicDefinition['Response']['data']['activity']['activityDescription'] + ' | Modifiers: ' + weeklyHeroicDefinition['Response']['data']['activity']['skulls'][1]['displayName']
    else:
        return "weylin lied to me, get good scrub."

@hook.command('triumph')
def triumph(text, bot):
    api_key = bot.config.get("api_keys", {}).get("destiny", None)

    HEADERS = {"X-API-Key":api_key}

    
    id = text.strip()

    r = requests.get("http://www.bungie.net/Platform/User/SearchUsers/?q=" + str(id), headers=HEADERS);

    userID = r.json()

    userIDHash = userID['Response'][0]['membershipId']
    userName = userID['Response'][0]['displayName']

    r = requests.get("https://www.bungie.net/platform/User/GetBungieAccount/" + str(userIDHash) + "/254/", headers=HEADERS);
 
    userHash = r.json()

    membershipType =  userHash['Response']['destinyAccounts'][0]['userInfo']['membershipType']

    membershipId = userHash['Response']['destinyAccounts'][0]['userInfo']['membershipId']

    membershipType2 = str(membershipType)
    membershipId2 = str(membershipId)

    r = requests.get("https://www.bungie.net/platform/Destiny/" + membershipType2 + "/Account/" + membershipId2 + "/Triumphs/", headers=HEADERS);

    triumphHash = r.json()

    triumph0 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][0]['complete']
    triumph1 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][1]['complete']
    triumph2 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][2]['complete']
    triumph3 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][3]['complete']
    triumph4 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][4]['complete']
    triumph5 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][5]['complete']
    triumph6 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][6]['complete']
    triumph7 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][7]['complete']
    triumph8 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][8]['complete']
    triumph9 = triumphHash['Response']['data']['triumphSets'][0]['triumphs'][9]['complete']

    triumphcheck = triumph0 + triumph1 + triumph2 + triumph3 + triumph4 + triumph5 + triumph6 + triumph7 + triumph8 + triumph9
    triumphStatus = int(triumphcheck)

    if triumphStatus == 10:
        return userName + "\'s Year One Triumph is complete!"
    else:
        return userName + "\'s Year One Triumph is not complete!"

@hook.command('xur')
def xur(text, bot):
    api_key = bot.config.get("api_keys", {}).get("destiny", None)

    HEADERS = {"X-API-Key":api_key}

    r = requests.get("https://www.bungie.net/platform/Destiny/Advisors/Xur/?definitions=true", headers=HEADERS);

    xurStock = r.json()

    xurExoticHash0 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['itemHash'])

    xurExoticName01 = str(xurStock['Response']['definitions']['items'][xurExoticHash0]['itemName'])

    xurExoticStatHash01 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][1]['statHash'])
    xurExoticStatName01 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash01]['statName'])
    xurExoticStatValue01 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][1]['value'])


    xurExoticStatHash02 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][2]['statHash'])
    xurExoticStatName02 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash02]['statName'])
    xurExoticStatValue02 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][2]['value'])


    xurExoticStatHash03 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][3]['statHash'])
    xurExoticStatName03 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash03]['statName'])
    xurExoticStatValue03 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][0]['item']['stats'][3]['value'])


    xurExoticStatName0 = xurStock['Response']['definitions']['stats'][xurExoticStatHash01]['statName']


    xurExoticHash1 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['itemHash'])

    xurExoticName11 = str(xurStock['Response']['definitions']['items'][xurExoticHash1]['itemName'])

    xurExoticStatHash11 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][1]['statHash'])
    xurExoticStatName11 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash11]['statName'])
    xurExoticStatValue11 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][1]['value'])

    xurExoticStatHash12 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][2]['statHash'])
    xurExoticStatName12 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash12]['statName'])
    xurExoticStatValue12 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][2]['value'])

    xurExoticStatHash13 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][3]['statHash'])
    xurExoticStatName13 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash13]['statName'])
    xurExoticStatValue13 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][1]['item']['stats'][3]['value'])

    xurExoticStatName1 = xurStock['Response']['definitions']['stats'][xurExoticStatHash11]['statName']


    xurExoticHash2 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['itemHash'])

    xurExoticName21 = str(xurStock['Response']['definitions']['items'][xurExoticHash2]['itemName'])

    xurExoticStatHash21 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][1]['statHash'])
    xurExoticStatName21 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash21]['statName'])
    xurExoticStatValue21 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][1]['value'])

    xurExoticStatHash22 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][2]['statHash'])
    xurExoticStatName22 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash22]['statName'])
    xurExoticStatValue22 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][2]['value'])

    xurExoticStatHash23 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][3]['statHash'])
    xurExoticStatName23 = str(xurStock['Response']['definitions']['stats'][xurExoticStatHash23]['statName'])
    xurExoticStatValue23 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][2]['item']['stats'][3]['value'])

    xurExoticStatName2 = xurStock['Response']['definitions']['stats'][xurExoticStatHash21]['statName']

    xurExoticHash3 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][3]['item']['itemHash'])
    xurExoticName31 = str(xurStock['Response']['definitions']['items'][xurExoticHash3]['itemName'])

    xurExoticHash4 = str(xurStock['Response']['data']['saleItemCategories'][0]['saleItems'][5]['item']['itemHash'])
    xurExoticName41 = str(xurStock['Response']['definitions']['items'][xurExoticHash4]['itemTypeName'])

    return '\x030,1 Armor \x030,14 ' + xurExoticName01 + ' (' + xurExoticStatName01[:3] + ': ' + xurExoticStatValue01 + ', ' + xurExoticStatName02[:3] + ': ' + xurExoticStatValue02 + ', ' + xurExoticStatName03[:3] + ': ' + xurExoticStatValue03 + ')' + ', ' + xurExoticName11 + ' (' + xurExoticStatName11[:3] + ': ' + xurExoticStatValue11 + ', ' + xurExoticStatName12[:3] + ': ' + xurExoticStatValue12 + ', ' + xurExoticStatName13[:3] + ': ' + xurExoticStatValue13 + ')' + ', ' + xurExoticName21 + ' (' + xurExoticStatName21[:3] + ': ' + xurExoticStatValue21 + ', ' + xurExoticStatName22[:3] + ': ' + xurExoticStatValue22 + ', ' + xurExoticStatName23[:3] + ': ' + xurExoticStatValue23 + ') ' + '\x030,1 Weapon \x030,14 ' + xurExoticName31 + ' \x030,1 Engram \x030,14 ' + xurExoticName41






