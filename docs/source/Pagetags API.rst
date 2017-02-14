Pagetags API
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. http:post:: /auth

   Create an access token using the user's credentials

   **Example request**:

   .. sourcecode:: http

      POST /auth HTTP/1.1
      Host: localhost:5000
      Accept: application/json
      Content-Type: application/json

      {
          "username": "john",
          "password": "doe"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
        "access_token": "the.jwt.token"
      }

   :statuscode 200: no error
   :statuscode 401: invalid user credentials

.. http:get:: /api/v1/tags

   Return the available tags

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/tags HTTP/1.1
      Host: localhost:5000
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      ["tag1", "tag2", "tag3"]

   :reqheader Authorization: The JWT token

   :statuscode 200: no error
   :statuscode 401: invalid user credentials

.. http:get:: /api/v1/tag/(str:tag)

   Return the posts for `tag`

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/tag/tag1 HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "has_more": false,
          "page": 1,
          "per_page": 10,
          "posts": [
              {
                  "added_at": "2016/11/05 17:44:50",
                  "id": 11,
                  "tags": [
                      "tag1",
                      "tag2"
                  ],
                  "title": "test post 1",
                  "url": "http://example.com/post_1"
              },
              {
                  "added_at": "2016/11/05 17:44:43",
                  "id": 10,
                  "tags": [
                      "tag1",
                      "tag3"
                  ],
                  "title": "test post 2",
                  "url": "http://example.com/post_2"
              },
          ],
          "tag_id": 15
      }

   :reqheader Authorization: The JWT token

   :query page: page number
   :query per_page: posts per page

   :statuscode 200: no error
   :statuscode 404: the tag doesn't exist
   :statuscode 401: invalid user credentials

.. http:get:: /api/v1/posts

   Return the saved posts

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/posts HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "has_more": false,
          "page": 1,
          "per_page": 10,
          "posts": [
              {
                  "added_at": "2017/01/14 18:08:30",
                  "id": 15,
                  "tags": [
                      "type__article",
                      "cat__programming",
                      "topic__programming__web"
                  ],
                  "title": "I am a legend \u2013 hacking Hearthstone using statistical learning methods",
                  "url": "https://www.elie.net/publication/i-am-a-legend-hacking-hearthstone-using-statistical-learning-method"
              },
              {
                  "added_at": "2017/01/14 18:05:46",
                  "id": 14,
                  "tags": [
                      "type__article",
                      "cat__science"
                  ],
                  "title": "Overlooked molecules could revolutionise our understanding of the immune system",
                  "url": "http://www3.imperial.ac.uk/newsandeventspggrp/imperialcollege/newssummary/news_19-10-2016-17-31-5"
              }
          ]
      }

   :reqheader Authorization: The JWT token

   :query page: page number
   :query per_page: posts per page

   :statuscode 200: no error
   :statuscode 401: invalid user credentials

.. http:post:: /api/v1/posts

   Create a post

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/posts HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token
      Content-Type: application/json

      {
          "title": "post title",
          "url": "http://www.example.com/post_1",
          "tags": ["tag1", "tag2"]
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "id": 1
      }

   :reqheader Authorization: The JWT token

   :statuscode 200: no error
   :statuscode 401: invalid user credentials

.. http:get:: /api/v1/urls

   Return the saved posts for a given url

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/urls?url=https://www.example.com/post_1 HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "has_more": false,
          "page": 1,
          "per_page": 10,
          "posts": [
              {
                  "added_at": "2017/01/14 18:08:30",
                  "id": 15,
                  "tags": [
                      "tag1",
                      "tag2"
                  ],
                  "title": "Post title",
                  "url": "https://www.example.com/post_1"
              }
          ],
          "url_id": 13
      }

   :reqheader Authorization: The JWT token

   :query url: the url to use
   :query page: page number
   :query per_page: posts per page

   :statuscode 200: no error
   :statuscode 404: the url doesn't exist
   :statuscode 401: invalid user credentials

.. http:get:: /api/v1/post/(int:post_id)

   Return the post with the given `post_id`

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/post/123 HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "added_at": "2017-01-14 18:08:30.672532",
          "id": 15,
          "tags": [
              "tag1",
              "tag2"
          ],
          "title": "post title",
          "url": "http://www.example.com/post_1"
      }

   :reqheader Authorization: The JWT token

   :statuscode 200: no error
   :statuscode 404: the post with the given id doesn't exist
   :statuscode 401: invalid user credentials

.. http:put:: /api/v1/post/(int:post_id)

   Update the post with the given `post_id`

   **Example request**:

   .. sourcecode:: http

      PUT /api/v1/post/123 HTTP/1.1
      Host: localhost:5000
      Authorization: JWT the.jwt.token
      Content-Type: application/json

      {
         "url": "http://www.example.com/post_1",
         "title": "post title",
         "tags": ["tag1", "tag2"]
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/javascript

      {
          "added_at": "2017-01-14 18:08:30.672532",
          "id": 15,
          "tags": [
              "tag1",
              "tag2"
          ],
          "title": "post title",
          "url": "http://www.example.com/post_1"
      }

   :reqheader Authorization: The JWT token

   :statuscode 200: no error
   :statuscode 404: the post with the given id doesn't exist
   :statuscode 401: invalid user credentials
