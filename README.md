# simpleAPI
This repository of implementation of **API** for *create*, *modify*, *delete* and *update* of entry in text file

## Installation
* serve.py file contains the code of the http-server.
* .env file contains what changes need to be made initially i.e., initial setup.
* file_store.txt contains the data.

   ### The `.env` Variables
   * **IP**: This field is the IP address. By default, it takes *localhost* as **IP**.
   * **PORT**: This field is the PORT. By default, it takes *7000* as **PORT**.

* After setting up the .env file, serve.py needs to be executed. By running this, it shows *"Server started Successfully!"* on a successful start.
* Now, Open the browser and type the API on the URL.

## Requirements
The different libraries in Python3 :
* http
* urllib
* re
* decouple

# Different API:
1.  **_http://localhost:7000/file_store.txt?action=list_**
    To **list** the data stored in the file_store.txt file.
   On success, it returns 200 and the data present in the file. If no string is present against the id, it
   means that there is no data.
   
2.  **_http://localhost:7000/file_store.txt?action=view&id={num}_**
   To **view** the data from the file where *id = given num* (without curly bracket).
   On success, it returns 200 and the data against the given id if the data is present otherwise "No
   Data Found!".
   
3.  **_http://localhost:7000/file_store.txt?action=delete&id={num}_**
   To **delete** the data from the file where *id = given num* (without curly bracket). On success, it
   returns 200 and "OK".
   
4.  **_http://localhost:7000/file_store.txt?action=create&string={string}_**
   To **create** the data in the file with *string = given string* (without curly bracket). On success, it
   returns 200 and "OK".
   
5.  **_http://localhost:7000/file_store.txt?action=update&id={num}&string={string}_**
   To **update/edit** the data present in the file with *string = given string* (without curly bracket) where
   *id = given num* (without curly bracket). On success, it returns 200 and "OK". 
   
#### Note:
* If no API matches, it returns 404 and "URL Not Found!".

### Instruction in the file:
 The Entries in the file should follow the following format:
```
1:string1
2:string2
```

