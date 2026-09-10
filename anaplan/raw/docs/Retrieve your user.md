---
title: "Retrieve your user"
source: "https://help.anaplan.com/retrieve-your-user-d5e7ae19-0a8a-44a7-a482-bdee7479e039"
author:
published:
created: 2026-09-09
description: "Retrieves your user based on your Anaplan authentication token."
tags:
  - "clippings"
---
English

This helps an integration confirm which account is making the request and validate the identity under which permissions are being applied.

GET

`/users/me`

`curl -X GET \   https://api.anaplan.com/2/0/users/me \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type:application/json'`

`{      "meta":{         "schema":"https://api.anaplan.com/2/0/objects/user"      },      "user":{         "id":"8a8b844a477d5da70147d150ee080b17",         "active":true,         "email":"a.user@anaplan.com",         "emailOptIn":true,         "firstName":"A",         "lastName":"User",         "customerId":"8b81da6f5fb6b75701604d6c950c05b1",         "lastLoginDate":"2017-09-07T08:05:37.000+0000"      },      "status":{         "code":200,         "message":"Success"      }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-your-user-d5e7ae19-0a8a-44a7-a482-bdee7479e039&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top

## Need more help?

[![](https://help.anaplan.com/images/browser-charts-icon.svg)](https://portal.anaplan.com/) [![](https://help.anaplan.com/images/register.svg)](http://portal.anaplan.com/csm?id=csm_registration) [![](https://help.anaplan.com/images/Call.svg)](https://support.anaplan.com/contact)

Disclaimer

We update Anapedia content regularly to provide the most up-to-date instructions.

## Privacy Preference Center

### Your Privacy

- Under "Do Not Sell or Share" laws, some uses of cookies may be considered “selling” or “sharing” of personal data. Anaplan applies an opt-out by default standard — no personal data is sold or shared unless you affirmatively choose to opt-in. You may opt-in by toggling on the Sell or Share my Personal Data option. You may also opt-in to individual categories of cookies by toggling on the Targeting, Functional, and Performance options.
	Cookies Details

Consent Leg.Interest

  

Select All