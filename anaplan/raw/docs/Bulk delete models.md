---
title: "Bulk delete models"
source: "https://help.anaplan.com/bulk-delete-models-e45461b7-075f-4643-9174-9c4c5519ad36"
author:
published:
created: 2026-09-09
description: "Use this call to delete one or more models in a workspace. The models must be closed before they can be deleted. Failure to delete one of the models for some reason, for example the calling user not having access to that model, will not affect the deletion of the rest of the specified models."
tags:
  - "clippings"
---
[Model information](https://help.anaplan.com/model-information-c2998f80-d007-4a36-aef0-485923a38045 "Model information")

Use this call to delete one or more models in a workspace. The models **must be closed** before they can be deleted. Failure to delete one of the models for some reason, for example the calling user not having access to that model, will not affect the deletion of the rest of the specified models.

This supports administrative cleanup or lifecycle management of models, but is destructive and should be used carefully.

**Note:**

- The user must be a workspace administrator in the specified workspace and have access to the specified models.
- This is a destructive action - be careful when deleting models.

POST

`/workspaces/{workspaceId}/bulkDeleteModels`

| **Parameter** | **Required** | **Type** | **Details** |
| --- | --- | --- | --- |
| **{workspaceId}** | Yes | String | The workspace ID to delete models in. **Example:** 75A40874E6B64FA3AE0743278996850F |

`curl -X POST 'https://api.anaplan.com/2/0/workspaces/{workspaceId}/bulkDeleteModels' \    -H 'Authorization: AnaplanAuthToken {anaplan_auth_token}'   -H 'Content-Type: application/json'   --data-raw '{      "modelIdsToDelete": ["<model_id_to_delete_1", "<model_id_to_delete_2" ...]   }'`

If your response is successful, you receive a **200 OK** HTTP status with a response body.

`Content-Type: application/json`

If all the specified models were successfully deleted:

`{      "meta":{         "schema": "https://api.anaplan.com/2/0/objects/bulkDeleteModelsResponse"      },      "status":{         "code": 200,         "message": "Success"      },      "modelsDeleted": 4,      "bulkDeleteModelsFailures": []   }`

When some of the models were not deleted, their ID will be shown alongside a message:

`{      "meta":{         "schema": "https://api.anaplan.com/2/0/objects/bulkDeleteModelsResponse"      },      "status":{         "code": 200,         "message": "Success"      },      "modelsDeleted": 1,      "bulkDeleteModelsFailures": [         {           "modelId": "BC24B51B39CF4701ACF7CBFD2ED93C36",           "message": "Model is open. Please close the model before trying again."          },         {           "modelId": "EA8467B737A144C5B73CD56BA86085A0",           "message": "Something went wrong. Deleting this model failed."         },         {           "modelId": "Incorrect_Model_Id",           "message": "Model ID does not exist."         }      ]   }`

| **Code** | **Message** | **Required amendments** |
| --- | --- | --- |
| 400 | Error parsing request body as JSON | Check you have all the right elements in the request body. |
|  | Unrecognised property detected | Ensure only the supported properties are included in the request body. |
|  | Expected mandatory field 'modelIdsToDelete' | Add the mandatory fields for the call to be successful. |
|  | Other messages | Specific messages may be returned to the user if the JSON request body is invalid. |
| 403 | Forbidden | Check if the user is a workspace administrator. |
| 404 | Not Found | Check if the workspace ID specified in the URL is correct. |

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fbulk-delete-models-e45461b7-075f-4643-9174-9c4c5519ad36&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>

Back to top