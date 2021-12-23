# aws-key-utility

## Installation

    ```console
        git clone https://github.com/nileshbhadana/aws-key-utility.git
    ```
    ```console
        cd aws-key-utility/
        chmod +x ./setup.sh
        ./setup.sh
    ```
## Usage:

- List AWS your keys:
    ```console
        awskey
    ```
    OR <br>

    To list keys for particular profile: 
    ```console
        awskey --profile dev
    ```

- Rotate AWS Access keys:
    ```console
        awskey --profile dev --rotate
    ```

- Delete AWS Access key:
    ```console
        awskey --delete <ACCESS KEY ID>
    ```