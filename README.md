This is a inventory management project for a sporting goods store implemented using Python Django framework.

a. Frontend- html5/css3

b. Backend- MySQL

DJango Framework Overview-

●	This framework is based on the Model View Template(MVT) pattern. 

●	Django web applications typically group the code that handles each of these steps into separate files as follows-

1.urls.py- A URL mapper is used to redirect HTTP requests to the appropriate view based on the request URL.

2.views.py- A view is a request handler function, which receives HTTP requests and returns HTTP responses. Views access the data needed to satisfy requests via models, and delegate the formatting of the response to templates.

3.models.py- Models are Python objects that define the structure of an application's data, and provide mechanisms to manage (add, modify, delete) and query records in the database. 

4.Templates- All templates are present in the templates directory. A template is a text file defining the structure or layout of a file (such as an HTML page), with placeholders used to represent actual content. A view can dynamically create an HTML page using an HTML template, populating it with data from a model.

