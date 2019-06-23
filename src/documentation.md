*API endpoints*

If the endpoint is marked as \[login-required\] please include token from `login` endpoint in `Authorization` header

* register:
    * url: `/register`
    * method: `POST`
    * data: 
        * `name`
        * `password`
        * `email`
        
* login:
    * url: `/login/<user email>`
    * method: `POST`
    * data:
        * `password`
    
    * returns:
        * `token: <token>`

* subscribe \[login-required\]
    * url: `/subscribe`
    * method: `post`
    * data:
        * `payment_token`
        * `plan`
        
* website \[login-required\]
    * url: `/website`
    * method: `post`
    * data:
        * `url`
        
 * website \[login-required\]
    * url: `/website/<pk>`
    * method: `update`
    * data:
        * `url`
        
 * website \[login-required\]
    * url: `/website/<pk>`
    * method: `delete`
