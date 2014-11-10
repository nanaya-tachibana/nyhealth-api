FORMAT: 1A
HOST: https://nyhealth.herokuapp.com

# nyhealth API
nyHealth RESTful API.

## Authentication
*nyHealth API* uses Token Authorization. Auth token should be included in the Authorization HTTP
header when access the resources which need authentication.

## Error States
The common [HTTP Response Status Codes](https://github.com/for-GET/know-your-http-well/blob/master/status-codes.md) are used.

# Group Auth

## Sign up [/api/signup]

### Register a new account [POST]
This action will create and return user's auth token.

**Parameters**
- `phone_number` (required) ... phone_number of a user
- `username` (required) ... name of a user.
- `password` (required) ... password of a user.

+ Request (application/json)

    + Body

            {
                "phone_number": "+8613120933987",
                "username": "aaa",
                "password": "123"
            }

+ Response 200 (application/json)

        {
            'url': 'http://testserver/api/users/1/',
            'id': 1,
            'auth_token': 'dfed649dde66e6b16c6f41e8108b3986223ecc12',
            'username': 'aaa',
            'phone_number': '+8613120933987",
            'profiles': {'url': 'http://testserver/api/profiles/1/',
            'profile_photo': '',
            'language': 'en',
            'timezone': 'UTC',
            'location': 'HK',
            'birthday': '1970-01-01'},
            'care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'outgoing_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'incoming_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'monitorings': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []}
        }


## Login [/api/login]
### Login [POST]
This action will create and return user's auth token.

**Parameters**
- `phone_number` (required) ... phone_number of a user
- `password` (required) ... password of a user.

+ Request (application/json)

    + Body

            {
                "phone_number": "+8613120933987",
                "password": "123"
            }

+ Response 200 (application/json)

        {
            'url': 'http://testserver/api/users/1/',
            'id': 1,
            'auth_token': 'dfed649dde66e6b16c6f41e8108b3986223ecc12',
            'username': 'aaa',
            'phone_number': '+8613120933987',
            'profiles': {'url': 'http://testserver/api/profiles/1/',
            'profile_photo': '',
            'language': 'en',
            'timezone': 'UTC',
            'location': 'HK',
            'birthday': '1970-01-01'},
            'care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'outgoing_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'incoming_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'monitorings': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []}
        }

## Logout [/api/logout]
### Logout [POST]
This action will delete user's auth token.

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204


# Group Vital
All vital signs which have been collected into database.

## Vital [/api/available_vitals/{pk}/]
### Attributes
+ `url` ... uri of a vital resource
+ `name` ... name of a vital sign
+ `reference_value` ... the normal value where the vital sign should usually be
+ `unit` ... measurement unit of a vital sign

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/available_vitals/3/",
                "name": "xxxx",
                "reference_value": "1111",
                "unit": "kg",
            }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `1`) ... ID of a vital

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Vital][]


## Vitals Collection [/api/available_vitals/]

+ Model (application/json)

    + Body

            {
                    'url': 'http://testserver/api/available_vitals/4/',
                    'name': 'aa',
                    'reference_value': '1'
                    'unit': 'kg'
                    }, {
                    'url': 'http://testserver/api/available_vitals/5/',
                    'name': 'bb',
                    'reference_value': '2'
                    'unit': 'kg'
                    }, {
                    'url': 'http://testserver/api/available_vitals/6/',
                    'name': 'cc',
                    'reference_value': '3'
                    'unit': 'kg'
                    }
            }


### List all available vitals in database [GET]

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Vitals Collection][]

### Add new vital signs into database [POST]
Note that request body should always be a list even if only one data need to be added.

**Parameters**:
+ `name` (required) ... name of a vital sign
+ `reference_value` (optional) ... normal value of a vital sign
+ `unit` (optional) ... measurement unit of a vital sign

**Permission**: Admin User

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

    + Body

            [{
                "name": "a",
                "reference_value": "111",
                'unit': 'kg'
            }, {
                "name": "b",
                "reference_value": "222",
                'unit': 'kg'
            }]

+ Response 201 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
            "name": "a",
            "reference_value": "111",
            'unit': 'kg'
            }, {
            "url": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
            "name": "b",
            "reference_value": "222",
            'unit': 'kg'
        }]


# Group User
Users related resources of the **Users API**

## User [/api/users/{pk}/]
A single User object with all its details.

### Attributes
+ `url` ... uri of a user resource
+ `username` ... name of a user
+ `phone_number` ... phone number of a user
+ `profiles` ... profiles of a user
+ `care_relations` ... relations of a user
+ `outgoing_care_requests`: outgoing requests of a user who has a pending care request for others
+ `incoming_care_requests`: incoming requests of a user form whom others has a pending care request

+ Model (application/json)

    + Body

            {
                'url': 'http://testserver/api/users/1/',
                'id': 1,
                'auth_token': 'dfed649dde66e6b16c6f41e8108b3986223ecc12',
                'username': 'aaa',
                'phone_number': '+8613120933987',
                'profiles': {'url': 'http://testserver/api/profiles/1/',
                'profile_photo': '',
                'language': 'en',
                'timezone': 'UTC',
                'location': 'HK',
                'birthday': '1970-01-01'},
                'care_relations': {
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []},
                'outgoing_care_relations': {
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []},
                'incoming_care_relations': {
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []},
                'monitorings': {
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []}
            }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `1`) ... ID of a user

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [User][]

### Partial Update [PATCH]
**Parameters**
+ `username` (optional) ... name of a user
+ `phone_number` (optional) ... phone number of a user
+ `password` (optional) ... password of a user

+ Parameters
    + pk (Int, required, `1`) ... ID of a user

+ Request(application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

### Remove [DELETE]
+ Parameters
    + pk (Int, required, `1`) ... ID of a user

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204

## Reset password [/api/password/reset/]

This action will send a vertification code to user via SMS.

** TODO **

## Reset password confirm [/api/password/reset/confirm]
This action will needs user's vertification code which is sended by us.

** TODO **

## Change password [/api/password/change/]
## Change password [POST]
**Parameters**
+ `new_password1` (required) ... new password
+ `new_password2` (required) ... should be the same as new_password1

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 201

## Invite [/api/invite/]
Create new accounts which can be used to invite others to use.
The relation between a created account and current user's account will be added automaticly.
### Create a new account [POST]
**Parameters**
- `phone_number` (required) ... phone_number of a user
- `username` (required) ... name of a user.
- `password` (required) ... password of a user.

+ Request (application/json)

    + Body

            {
                "phone_number": "+8613120933987",
                "username": "aaa",
                "password": "123"
            }

+ Response 200 (application/json)

        {
            'url': 'http://testserver/api/users/1/',
            'id': 1,
            'auth_token': 'dfed649dde66e6b16c6f41e8108b3986223ecc12',
            'username': 'aaa',
            'phone_number': '+8613120933987",
            'profiles': {'url': 'http://testserver/api/profiles/1/',
            'profile_photo': '',
            'language': 'en',
            'timezone': 'UTC',
            'location': 'HK',
            'birthday': '1970-01-01'},
            'care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'outgoing_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'incoming_care_relations': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []},
            'monitorings': {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []}
        }


## Search [/api/users/search/{?page}{?username}{?phone_number}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of users

+ Model (application/json)

    + Body

            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/users/2/",
                    "username": "zzc",
                    "profiles": {
                    "url": "https://nyhealth.herokuapp.com/api/settings/2/",
                    "language": "en",
                    "timezone": "UTC"
                    },
                    }, {
                    "url": "https://nyhealth.herokuapp.com/api/users/3/",
                    "username": "a",
                    "profiles": {
                    "url": "https://nyhealth.herokuapp.com/api/settings/3/",
                    "language": "en",
                    "timezone": "UTC"
                    },
                }]
            }

### Search Users [GET]
+ Parameters
    + page (Int, optional, `2`) ... page number of the result list
    + username (String, optional, `zzc`) ... name of the user
    + phone_number (String, optional, `+8618918276867`) ... phone number of the user

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Search][]



# Group User Profile
## Profile [/api/profiles/{pk}]
### Attributes
+ `url` ... uri of a user profile resource
+ `profile_photo` ... photo url
+ `language` ... default language
+ `timezone` ... time zone
+ `location` ... location
+ `birthday` ... birthday

+ Model (application/json)

        {
            'url': 'http://testserver/api/profiles/1/',
            'profile_photo': '',
            'language': 'en',
            'timezone': 'UTC',
            'location': 'HK',
            'birthday': 1970-01-01
        }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `2`) ... ID

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Profile][]

### Partial update [PATCH]
**Parameters**
+ `language` (optional) ... language
+ `profile_photo` ... photo url
+ `timezone` (optional) ... time zone
+ `location` (optional) ... location
+ `birthday` (optional) ... birthday

+ Parameters
    + pk (Int, required, `2`) ... ID

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200



# Group Notification

## Inbox [/api/inbox/{pk}]
### Attributes
+ `url` ... uri of a message resource
+ `id` ... id
+ `message_text` ... content of a message
+ `level` ... type of a message. INFO=20, REMINDER=30, WARNING=40
+ `tags` ... tags
+ `date` ... date when a message is sent

+ Model (application/json)

        {
            'url': 'http://testserver/api/inbox/2/',
            'id': 2,
            'message_text': u'aaa\u4e0a\u4f20\u4e86\u4ed6\u7684a\u6570\u636e, \u5feb\u53bb\u770b\u770b\u5427',
            'level': 20,
            'tags': u'',
            'date': u'2014-11-10T04:48:48.943606+00:00'
        }


### Read [GET]
Note that message will be deleted after being read.

+ Parameters
    + pk (Int, required, `2`) ... ID

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Inbox][]


## Inbox Collection [/api/inbox/{?page}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of messages

+ Model (application/json)

        {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {'url': 'http://testserver/api/inbox/2/',
                'id': 2,
                'message_text': 'aaa\u4e0a\u4f20\u4e86\u4ed6\u7684a\u6570\u636e, \u5feb\u53bb\u770b\u770b\u5427',
                'level': 20,
                'tags': '',
                'date': '2014-11-10T04:48:48.943606+00:00'},
                {'url': 'http://testserver/api/inbox/1/',
                'id': 1,
                'message_text': 'aaa\u4e0a\u4f20\u4e86\u4ed6\u7684a\u6570\u636e, \u5feb\u53bb\u770b\u770b\u5427',
                'level': 20,
                'tags': '',
                'date': '2014-11-10T04:48:48.941002+00:00'}
            ]
        }

### List all [GET]
+ Parameters
    + page (Int, required, `2`) ... page number

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Inbox Collection][]



# Group User Relations
User relations related resources of the **Relations API**

## Relation [/api/relations/{pk}/]
Detailed information about the relation between two arbitrary users
### Attributes
+ `url` ... uri of the relation resource
+ `user` ... uri of the user whrere the relation start
+ `to_user` ... uri of the user where the relation end
+ `description` ... a user defined description for the relation
+ `created` ... created time
+ `updated` ... last updated time

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/relations/2/",
                "user": "https://nyhealth.herokuapp.com/api/users/2/",
                "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                "description": "dad",
                "created": "2014-09-28T08:39:59.563Z",
                "updated": "2014-09-28T08:48:39.355Z"
            }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `2`) ... ID of a relation

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Relation][]

### Change description [PATCH]
**Parameters**
+ `description` (required) ... a short description for the relation.

+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

    + Body

            {
                "description": "mother"
            }

+ Response 201

### Delete [DELETE]
+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204


## Relations Collection [/api/relations/{?page}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of relations

+ Model (application/json)

    + Body

            {
                'COUNT': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/relations/2/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "description": "dad",
                    "created": "2014-09-28T08:39:59.563Z",
                    "updated": "2014-09-28T08:48:39.355Z"
                }, {
                    "url": "https://nyhealth.herokuapp.com/api/relations/6/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
                    "description": "mom",
                    "created": "2014-09-28T08:45:37.558Z",
                    "updated": "2014-09-28T08:48:47.406Z"
                }]
            }

### List all relations [GET]
+ Parameters
    + page (Int, optional, `2`) ... the page number of the result list

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Relations Collection][]

## Outgoing Relation [/api/relations/outgoings/{pk}]
The care relation requests sended by the user and not confirmed by the other side.
### Attributes
+ `url` ... uri of the relation resource
+ `user` ... uri of the user whrere the relation start
+ `to_user` ... the uri of the user where the relation end
+ `description` ... a user defined description for the relation
+ `created` ... created time
+ `updated` ... last updated time

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/relations/2/",
                "user": "https://nyhealth.herokuapp.com/api/users/2/",
                "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                "description": "dad",
                "created": "2014-09-28T08:39:59.563Z",
                "updated": "2014-09-28T08:48:39.355Z"
            }

### Retrieve[GET]
+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Outgoing Relation][]

### Delete [DELETE]
+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204

## Outgoing Relations Collection [/api/relations/outgoings/{?page}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of relations

+ Model (application/json)

    + Body

            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/relations/outgoings/1/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "description": "dad",
                    "created": "2014-09-28T08:39:59.563Z",
                    "updated": "2014-09-28T08:48:39.355Z"
                }, {
                    "url": "https://nyhealth.herokuapp.com/api/relations/outgoings/7/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
                    "description": "mom",
                    "created": "2014-09-28T08:45:37.558Z",
                    "updated": "2014-09-28T08:48:47.406Z"
                }]
            }

### List all outgoing relations [GET]
+ Parameters
    + page (Int, optional, `2`) ... the page number of the result list

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Outgoing Relations Collection][]

### Send a care request [POST]
**Parameters**
+ `to_user` (required) ... the uri of a user(e.g.,"https://nyhealth.herokuapp.com/api/users/2/")
+ `description` (optional) ... a short description for the relation.

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here


    + Body

            {
                "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                "description": "dad"
            }

+ Response 201

    [Outgoing Relation][]

## Incoming relation [/api/relations/incomings/{pk}]
The care relation request sended to the user and waiting for the user's confirmation
### Attributes
+ `url` ... uri of the relation resource
+ `user` ... uri of the user whrere the relation start
+ `to_user` ... uri of the user where the relation end
+ `description` ... a user defined description for the relation
+ `created` ... created time
+ `updated` ... last updated time

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/relations/2/",
                "user": "https://nyhealth.herokuapp.com/api/users/2/",
                "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                "description": "dad",
                "created": "2014-09-28T08:39:59.563Z",
                "updated": "2014-09-28T08:48:39.355Z"
            }

### Allow a relation request [PATCH]
+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 201

### Deny a relation request [DELETE]
+ Parameters
    + pk (Int, required, `1`) ... ID of a relation

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204

## Incoming Relations Collection [/api/relations/incomings/{?page}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of relations

+ Model (application/json)

    + Body

            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/relations/incomings/1/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "description": "",
                    "created": "2014-09-28T08:39:59.563Z",
                    "updated": "2014-09-28T08:48:39.355Z"
                }, {
                    "url": "https://nyhealth.herokuapp.com/api/relations/incomings/7/",
                    "user": "https://nyhealth.herokuapp.com/api/users/2/",
                    "to_user": "https://nyhealth.herokuapp.com/api/users/3/",
                    "description": "",
                    "created": "2014-09-28T08:45:37.558Z",
                    "updated": "2014-09-28T08:48:47.406Z"
                }]
            }

### List all incoming relations [GET]
+ Parameters
    + page (Int, optional, `2`) ... the page number of the result list

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

   [Incoming Relations Collection][]



# Group User Vitals
Vital records uploaded by the user.
## Vital Record [/api/vitals/{pk}/]
### Attributes
+ `url` ... uri of the vital record resource
+ `vital_name` ... name of the vital sign
+ `user` ... uri of the user who uploaded this record
+ `vital` ...  uri of the vital sign that this record recorded
+ `value` ... value of the vital sign
+ `created` .. created time
+ `updated` ... last updated time

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
                "vital_name": "a",
                "user": "https://nyhealth.herokuapp.com/api/users/1/",
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
                "value": "24",
                "created": "2014-09-28T15:58:36.274Z",
                "updated": "2014-09-28T15:58:36.274Z"
            }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `1`) ... ID of a vital record

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Vital Record][]

## Vital Records Collection [/api/vitals/{?page}{?since}{?vital}{?user}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of vital records

+ Model (application/json)

    + Body

            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
                    "vital_name": "a",
                    "user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
                    "value": "24",
                    "created": "2014-09-28T15:58:36.274Z",
                    "updated": "2014-09-28T15:58:36.274Z"
                }, {
                    "url": "https://nyhealth.herokuapp.com/api/vitals/2/",
                    "vital_name": "b",
                    "user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
                    "value": "25",
                    "created": "2014-09-28T15:59:36.274Z",
                    "updated": "2014-09-28T15:59:36.274Z"
                }]
            }

### List all uploaded vital records [GET]
+ Parameters
    + page (Int, optional, `2`) ... page number of the result list
    + since (Date, optional, `2014-08-09`) ... the date which the create time of returning records should be great than
      this should be a ISO 8601 style datetime string.
    + vital (Int, optional, `1`) ... id of which kind of vital sign related vital records will be returned
    + user (Int, optional, `1`) ... id of who's vital records will be returned
      if someone want to look another user's vital records, he need to be lucky in her care list, otherwise 403 will be returned.

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Vital Records Collection][]

### Upload vital records [POST]
**Parameters**
+ `vital` (required) ... the uri of the vital(e.g., "https://nyhealth.herokuapp.com/api/available_vitals/2/")
+ `value` (required) ... the value of the vital

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here

    + Body

            [{
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
                "value": "24"
            }, {
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
                "value": "25"
            }]

+ Response 201 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
            "value": "24",
            "created": "2014-09-28T15:58:36.274Z",
            "updated": "2014-09-28T15:58:36.274Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "vital_name": "b",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
            "value": "25",
            "created": "2014-09-28T15:59:36.274Z",
            "updated": "2014-09-28T15:59:36.274Z"
        }]

## One Page Vital Records [/api/vitals/one_page/{?since}{?vital}{?user}]
Return all vital records in only one page.

+ Model (application/json)

    + Body

            [{
            "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
            "value": "24",
            "created": "2014-09-28T15:58:36.274Z",
            "updated": "2014-09-28T15:58:36.274Z"
            }, {
            "url": "https://nyhealth.herokuapp.com/api/vitals/2/",
            "vital_name": "b",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
            "value": "25",
            "created": "2014-09-28T15:59:36.274Z",
            "updated": "2014-09-28T15:59:36.274Z"
            }]


### List all records in one page [GET]
+ Parameters
    + since (Date, optional, `2014-08-09`) ... the date which the create time of returning records should be great than
      this should be a ISO 8601 style datetime string.
    + vital (Int, optional, `1`) ... id of which kind of vital sign related vital records will be returned
    + user (Int, optional, `1`) ... id of who's vital records will be returned
      if someone want to look another user's vital records, he need to be lucky in her care list, otherwise 403 will be returned.

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [One Page Vital Records][]


# Group User Monitoring
A bunch of vitals which are cared by a user.
## Monitoring [/api/vitals/monitorings/{pk}/]
### Attributes
+ `url` ... uri of the vital record resource
+ `vital_name` ... name of the vital sign
+ `user` ... uri of the user who uploaded this record
+ `vital` ...  uri of the vital sign
+ `level` ... dangerous level for the vital of the user
+ `created` .. created time
+ `updated` ... last updated time

+ Model (application/json)

    + Body

            {
                "url": "https://nyhealth.herokuapp.com/api/vitals/1/",
                "vital_name": "a",
                "user": "https://nyhealth.herokuapp.com/api/users/1/",
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
                "level": 0,
                "created": "2014-09-28T15:58:36.274Z",
                "updated": "2014-09-28T15:58:36.274Z"
            }

### Retrieve [GET]
+ Parameters
    + pk (Int, required, `1`) ... ID of a vital

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Monitoring][]

### Delete [DELETE]
+ Parameters
    + pk (Int, required, `1`) ... ID of a vital

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 204

## Monitorings Collection [/api/vitals/monitorings/{?page}]
### Attributes
+ `count` ... total number of the results
+ `next` ... url of next page
+ `previous` ...  url of previous page
+ `results` ... a list of Monitorings

+ Model (application/json)

    + Body

            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [{
                    "url": "https://nyhealth.herokuapp.com/api/vitals/monitorings/1/",
                    "vital_name": "a",
                    "user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
                    "level": 0,
                    "created": "2014-09-28T16:26:17.253Z",
                    "updated": "2014-09-28T16:26:17.253Z"
                }, {
                    "url": "https://nyhealth.herokuapp.com/api/vitals/monitorings/2/",
                    "vital_name": "2",
                    "user": "https://nyhealth.herokuapp.com/api/users/1/",
                    "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
                    "level": 1,
                    "created": "2014-09-28T16:27:01.245Z",
                    "updated": "2014-09-28T16:27:01.245Z"
                }]
            }

### List all Monitorings [GET]
+ Parameters
    + page (Int, optional, `2`) ... the page number of the result list

+ Request

    + Headers

            Authorization: Token replace_with_your_token_string_here

+ Response 200

    [Monitorings Collection][]

### add vitals to monitorings [POST]
**Parameters**
+ `vital` (required) ... the uri of a vital sign(e.g., "https://nyhealth.herokuapp.com/api/available_vitals/2/")

+ Request (application/json)

    + Headers

            Authorization: Token replace_with_your_token_string_here


    + Body

            [{
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
            }, {
                "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
            }
            ]

+ Response 201 (application/json)

        [{
            "url": "https://nyhealth.herokuapp.com/api/vitals/monitorings/1/",
            "vital_name": "a",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/1/",
            "level": 0,
            "created": "2014-09-28T16:26:17.253Z",
            "updated": "2014-09-28T16:26:17.253Z"
        }, {
            "url": "https://nyhealth.herokuapp.com/api/vitals/monitorings/2/",
            "vital_name": "2",
            "user": "https://nyhealth.herokuapp.com/api/users/1/",
            "vital": "https://nyhealth.herokuapp.com/api/available_vitals/2/",
            "level": 1,
            "created": "2014-09-28T16:27:01.245Z",
            "updated": "2014-09-28T16:27:01.245Z"
        }]
