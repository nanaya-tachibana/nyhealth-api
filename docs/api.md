FORMAT: 1A
HOST: https://nyhealth.herokuapp.com

# nyhealth API
nyhealth RESTful API.

# Group Token
Auth token
## Token [/api/token]
### Retrieve auth token [POST]
Get user's auth token
+ Request

    Parameters:

    + `username` (required) ... the name of user.
    + `password` (required) ... the password of user.

    + Body

            {
                "username": "nanaya",
                "password": "123"
            }

+ Response 200 (application/json)

        {"token": "3c47427c6dd300477ab46596ae50be3eb728ad52"}


# Group Vital
Available vital signs
## Vitals Collection [/api/vitals/]
### List all vitals [GET]
+ Request

    + Permission
      All

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "name": "a",
            "reference_value": ""
            }, {
            "url": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "name": "b",
            "reference_value": ""
        }]

### Create a vital [POST]
+ Request (application/json)

    Parameters:

    + `name` (required) ... the name of a vital sign.
    + `reference_value` (optional) ... the reference value of a vital sign.

    + Permission
      Admin user

    + Body

            {
                "name": "xxxx",
                "reference_value": "1111"
            }

+ Response 201 (application/json)


            {"url": "https://nyhealth.herokuapp.com/api/vitals/3/", "name": "xxxx", "reference_value": "1111"}


## Vital [/vitals/{pk}/]
### Retrieve a vital [GET]
+ Request

    + Permission
      Admin user

+ Response 200 (application/json)

        {"url": "https://nyhealth.herokuapp.com/api/vitals/3/", "name": "xxxx", "reference_value": "1111"}


# Group Users
Users related resources of the **Users API**

## Users Collection [/api/users/]
### List all Users [GET]
+ Request

    + Permission
      Admin user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/2/",
            "username": "zzc",
            "phone_number": "+8618918276877",
            "settings": {
                "url": "https://nyhealth.herokuapp.com/api/users/2/settings/",
                "language": "en",
                "timezone": "UTC"
                },
                "care_relations": [],
                "outgoing_care_requests": [],
                "incoming_care_requests": []}, {
            "url": "https://nyhealth.herokuapp.com/api/users/3/",
            "username": "a",
            "phone_number": "+8615121030003",
            "settings": {
                "url": "https://nyhealth.herokuapp.com/api/users/3/settings/",
                "language": "en",
                "timezone": "UTC"
                },
            "care_relations": [],
            "outgoing_care_requests": [],
            "incoming_care_requests": []
        }]

### Create a User [POST]
+ Request (application/json)

    Parameters:

    + `username` (required) ... the name of a user.
    + `phone_number` (required) ... the phone number of a user.
    + `password` (required) ... the password of a user.

    + Body

            {
                "username": "zzc"
                "password": "zzchi"
                "phone_number": "+8613122222222"
            }

+ Response 201 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/2/",
            "username": "zzc",
            "phone_number": "+8613122222222"
            "settings": {
                "url": "https://nyhealth.herokuapp.com/api/users/2/settings/",
                "language": "en",
                "timezone": "UTC"
                },
            "care_relations": [],
            "outgoing_care_requests": [],
            "incoming_care_requests": []
        }


## User [/users/{pk}/]
A single User object with all its details
### Retrieve a User [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/2/",
            "username": "zzc",
            "phone_number": "+8618918276877",
            "settings": {
                "url": "https://nyhealth.herokuapp.com/api/users/2/settings/",
                "language": "en",
                "timezone": "UTC"
                },
                "care_relations": [],
                "outgoing_care_requests": [],
                "incoming_care_requests": []}, {
            "url": "https://nyhealth.herokuapp.com/api/users/3/",
            "username": "a",
            "phone_number": "+8615121030003",
            "settings": {
                "url": "https://nyhealth.herokuapp.com/api/users/3/settings/",
                "language": "en",
                "timezone": "UTC"
                },
            "care_relations": [],
            "outgoing_care_requests": [],
            "incoming_care_requests": []
        }]

### Partial update a User [PATCH]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200

### Remove a User [DELETE]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 204


# Group User Relations
User relations related resources of the **Relations API**
## User Relations Collection [/api/users/{user_id}/relations/]
User's confirmed relations.
### List all relations [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/2/relations/2/",
            "user": "https://nyhealth.herokuapp.com/api/users/2/",
            "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
            "created": "2014-09-28T08:39:59.563Z",
            "updated": "2014-09-28T08:48:39.355Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/2/relations/6/",
            "user": "https://nyhealth.herokuapp.com/api/users/2/",
            "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
            "created": "2014-09-28T08:45:37.558Z",
            "updated": "2014-09-28T08:48:47.406Z"
        }]

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/1/relations/outgoings/1/",
            "user": 1,
            "to_user": "https://nyhealth.herokuapp.com/api/users/2/",
            "created": "2014-09-28T08:39:59.526Z",
            "updated": "2014-09-28T08:39:59.526Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/1/relations/outgoings/3/",
            "user": 1,
            "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
            "created": "2014-09-28T08:40:06.943Z",
            "updated": "2014-09-28T08:40:06.943Z"
        }]


## User Relation [/api/users/{user_id}/relations/{pk}/]
### Retrieve a relation [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/2/relations/2/",
            "user": "https://nyhealth.herokuapp.com/api/users/2/",
            "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
            "created": "2014-09-28T08:39:59.563Z",
            "updated": "2014-09-28T08:48:39.355Z"
        }

### change description [PATCH]
+ Request (application/json)

    Parameters:

    + `description` (optional) ... a short description for the relation.

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string


    + Body

            {
                "description": "mother"
            }

+ Response 201

### Delete a relation [DELETE]
+ Request (application/json)

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 204


## User Outgoing Relations Collection [/users/{user_id}/relations/outgoings/]
User's outgoing relations requests.
### List all outgoing relations [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/1/relations/outgoings/1/",
            "user": 1,
            "to_user": "https://nyhealth.herokuapp.com/api/users/2/",
            "created": "2014-09-28T08:39:59.526Z",
            "updated": "2014-09-28T08:39:59.526Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/1/relations/outgoings/3/",
            "user": 1,
            "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
            "created": "2014-09-28T08:40:06.943Z",
            "updated": "2014-09-28T08:40:06.943Z"
        }]

### Send an asking relation request [POST]
Send a request to another user to build a relation.

+ Request (application/json)

    Parameters:

    + `to_user` (required) ... the hyperlink of a user. for example, "https://nyhealth.herokuapp.com/api/users/2/".
    + `description` (optional) ... a short description for the relation.


    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string


    + Body

            {
                "to_user": "https://nyhealth.herokuapp.com/api/users/2/",
                "description": "mother"
            }

+ Response 201 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/3/relations/outgoings/5/",
            "user": "3",
            "to_user": "https://nyhealth.herokuapp.com/api/users/2/",
            "description": "mother",
            "created": "2014-09-28T08:45:37.501Z",
            "updated": "2014-09-28T08:45:37.501Z"
        }


## User Outgoing relation [/users/{user_id}/relations/outgoings/{pk}]
### Retrieve an outgoing relation [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/3/relations/outgoings/5/",
            "user": "3",
            "to_user": "https://nyhealth.herokuapp.com/api/users/2/",
            "description": "mother",
            "created": "2014-09-28T08:45:37.501Z",
            "updated": "2014-09-28T08:45:37.501Z"
        }

### Delete an outgoing relation [DELETE]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 204

## User Incoming Relations Collection [/users/{user_id}/relations/incomings/]
User's incoming relations requests.
### List all incoming relations [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/2/relations/incomings/2/",
            "user": 2,
            "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
            "created": "2014-09-28T08:39:59.563Z",
            "updated": "2014-09-28T08:39:59.563Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/2/relations/incomings/6/",
            "user": 2,
            "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
            "created": "2014-09-28T08:45:37.558Z",
            "updated": "2014-09-28T08:45:37.558Z"
        }]

## User Incoming relation [/users/{user_id}/relations/incomings/{pk}]
### Allow an relation request [PATCH]
Allow another user's asking relation request.

+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 201

### Deny an relation request [DELETE]
Deny another user's asking relation request.

+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 204

# Group User Vitals
## User vitals Collection [/users/{user_id}/vitals/]
User's uploaded vital data.
### List all uploaded vitals [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/1/vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "value": "24",
            "created": "2014-09-28T15:58:36.274Z",
            "updated": "2014-09-28T15:58:36.274Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/1/vitals/2/",
            "vital_name": "b",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "value": "25",
            "created": "2014-09-28T15:59:36.274Z",
            "updated": "2014-09-28T15:59:36.274Z"
        }]

### Upload a vital data [POST]
+ Request (application/json)

    Parameters:

    + `vital` (required) ... the hyperlink of a vital. for example, "https://nyhealth.herokuapp.com/api/vitals/2/".
    + `value` (optional) ... the value of the vital.


    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string


    + Body

            {
                "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
                "value": 24
            }

+ Response 201 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/1/vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "value": "24",
            "created": "2014-09-28T15:58:36.274Z",
            "updated": "2014-09-28T15:58:36.274Z"
        }


## User vital [/users/{user_id}/vitals/{pk}/]
### Retrieve a vital data record [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/1/vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "value": "24",
            "created": "2014-09-28T15:58:36.274Z",
            "updated": "2014-09-28T15:58:36.274Z"
        }


# Group User Care Vitals
## User cared vitals Collection [/users/{user_id}/cared_vitals/]
### List all cared vitals [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/users/1/cared_vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "created": "2014-09-28T16:26:17.253Z",
            "updated": "2014-09-28T16:26:17.253Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/users/1/cared_vitals/2/",
            "vital_name": "2",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "created": "2014-09-28T16:27:01.245Z",
            "updated": "2014-09-28T16:27:01.245Z"
        }]

### add a cared vital [POST]
+ Request (application/json)

    Parameters:

    + `vital` (required) ... the hyperlink of a vital. for example, "https://nyhealth.herokuapp.com/api/vitals/2/".


    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string


    + Body

            {
                "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
            }

+ Response 201 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/1/cared_vitals/2/",
            "vital_name": "2",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "created": "2014-09-28T16:27:01.245Z",
            "updated": "2014-09-28T16:27:01.245Z"
        }


## User cared vital [/users/{user_id}/cared_vitals/{pk}/]
### Retrieve a cared vital [GET]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 200 (application/json)

        {
            "url": "https://nyhealth.herokuapp.com/api/users/1/cared_vitals/2/",
            "vital_name": "2",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "created": "2014-09-28T16:27:01.245Z",
            "updated": "2014-09-28T16:27:01.245Z"
        }

### Delete a cared vital [DELETE]
+ Request

    + Permission
      Authenticated user

    + Headers

            Authorization: Token token string

+ Response 204
