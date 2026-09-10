---
title: "Retrieve user list"
source: "https://help.anaplan.com/retrieve-user-list-24b4492c-3dda-4cae-ae07-7ccdb134a433"
author:
published:
created: 2026-09-09
description: "Retrieves a list of users."
tags:
  - "clippings"
---
English

**Note:** Touse this call, you must be a [Workspace Administrator](https://help.anaplan.com/6ed59998-91ce-4a3a-ab64-8f57d1c1ce09), or have any [tenant-level access role](https://help.anaplan.com/0abbe291-3dcd-4b79-b36e-7cb05cd21975).

GET

`/users?sort=%2BemailAddress`

| **Parameter** | **Details** |
| --- | --- |
| `sort` |  |

`curl -X GET \   https://api.anaplan.com/2/0/users?sort=%2BemailAddress \   -H 'authorization: AnaplanAuthToken {anaplan_auth_token}' \   -H 'Content-Type:application/json'`

`{      "meta":{         "schema":"https://api.anaplan.com/2/0/objects/user"      },      "user":{         "id":"8a8196a55b193fa0015b1e57f3da172c",         "active":true,         "email":"a.user@company.com",         "emailOptIn":true,         "firstName":"A",         "lastName":"User",         "lastLoginDate":"2017-09-07T08:05:37.000+0000"      },      "status":{         "code":200,         "message":"Success"      }   }`

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fretrieve-user-list-24b4492c-3dda-4cae-ae07-7ccdb134a433&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

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