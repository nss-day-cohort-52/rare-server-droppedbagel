from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views.subscription_requests import delete_subscription, get_subscriptions, get_users_subs

from views.posttag_request import create_entrytag
from views.subscription_requests import get_subscriptions, get_users_subs

from views.user import create_user, login_user, get_all_users, get_single_user
from views.category_requests import create_category, delete_category, edit_category
from views.user import create_user, login_user
from views import get_all_categories, create_subscription
from views.posts import create_post, delete_post, get_all_posts, get_single_post, update_post
from views import (get_all_tags, get_single_tag, create_tag, delete_tag, update_tag,
                   get_all_comments_by_post, get_all_comments, get_single_comment, create_comment, 
                   delete_comment, update_comment, get_all_reactions, get_single_reaction, 
                   create_reaction, delete_reaction, update_reaction, get_all_post_reactions, 
                   get_single_post_reaction, create_post_reaction, delete_post_reaction, 
                   update_post_reaction)


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)

        response = {}
        parsed = self.parse_url()
        if len(parsed) == 2:
            ( resource, id ) = parsed
            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            if resource == "posts":
                if id is not None: 
                    response = get_single_post(id)
                else: 
                    response = get_all_posts()
            if resource == "tags":
                if id is None:
                    response = get_all_tags()
                else:
                    response = get_single_tag(id)
                    
            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)
                else:
                    response = get_all_comments()
            if resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_subscriptions()}"
            if resource == "reactions":
                if id is not None:
                    response = get_single_reaction(id)
                else:
                    response = get_all_reactions()
            if resource == "postreactions":
                if id is not None:
                    response = get_single_post_reaction(id)
                else:
                    response = get_all_post_reactions()                
        
        elif len(parsed) == 3:
            (resource, key, value) = parsed
            if resource == "comments" and key == "post_id":
                response = get_all_comments_by_post(value)
            if resource == "subscriptions" and key == "user_id":
                response = get_users_subs(value)
        
        self.wfile.write(response.encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == "posts":
            response = create_post(post_body)
        if resource == "tags":
            response = create_tag(post_body)
        if resource == "comments":
            response = create_comment(post_body)
        if resource == "subscriptions":
            response = create_subscription(post_body)
        if resource == "posttags":
            response = create_entrytag(post_body)
        if resource == "reactions":
            response = create_reaction(post_body)
        if resource == "postreactions":
            response = create_post_reaction(post_body)

        self.wfile.write(response.encode())
        
        

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        (resource, id) = self.parse_url()
        success = False
        if resource == "categories":
            success = edit_category(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)
        if resource == "reactions":
            success = update_reaction(id, post_body)
        if resource == "postreactions":
            success = update_post_reaction(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())
        pass

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        (resource, id) = self.parse_url()
        if resource == "categories":
            delete_category(id)
        if resource == "posts":
            delete_post(id)
        if resource == "tags":
            delete_tag(id)
        if resource == "comments":
            delete_comment(id) 
        if resource == "reactions":
            delete_reaction(id)
        if resource == "postreactions":
            delete_post_reaction(id) 
        self.wfile.write("".encode())
        if resource == "subscriptions":
            delete_subscription(id)
        pass

        
        
       
        

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
