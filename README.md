# Auto Mosaic

### Requirements

* Huawei Account

  ```json
  {
      "auth": {
          "identity": {
              "methods": ["password"],
              "password": {
                  "user": {
                      "name": "##username##",
                      "password": "password",
                      "domain": {
                          "name": "##username##"
                      }
                  }
              }
          },
          "scope": {
              "project": {
                  "name": "##project_name##"
              }
          }
      }
  }
  ```

  Save ↑ as file `auth_data` into `$PROJECT_ROOT/data/iam`.

  Save your api url as file `api_url` into `$PROJECT_ROOT/data/iam`.

  Modify your own IAM auth token url w.r.t. your project region at the entrance of this program.

  **Do not make your secrets known to the public**

  File structure should be like this:

  ```
  ./
  ├── README.md
  ├── auth.py
  ├── data
  │   ├── VOC2007test(this is image data folder)
  │   └── iam
  │       ├── 20191225041659231430.aidate
  │       ├── api_url(only content is an url)
  │       └── auth_data
  ├── mosaix.py
  └── utils.py
  ```

* Python 3.7
  * opencv-python
  * numpy
  * matplotlib
  * pillow
  
* Modify your own data path (like `./data/VOC2007test/...`) in function `main`

### Run

Run `python mosaix.py`

