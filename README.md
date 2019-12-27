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
  │   ├── cache
  │   ├── iam
  │   │   ├── 20191226233557982276.aidate
  │   │   ├── api_url((each line of content is an url))
  │   │   └── auth_data
  │   ├── output
  │   │   ├── xxx-out.mp4
  │   │   └── val
  │   ├── temp
  │   ├── test(this is test set folder)
  │   │   ├── Annotations
  │   │   ├── ImageSets
  │   │   └── JPEGImages
  │   └── video
  │       └── xxx-in.mp4
  ├── mosaix.py
  ├── test.py
  ├── utils.py
  ├── val.py
  └── voc_eval.py
  ```

* Python 3.7
  * opencv-python
  * numpy
  * matplotlib
  * pillow
  
* Modify your own data path (like `./data/VOC2007test/...`) in function `main`

### Run

Run `python mosaix.py`

