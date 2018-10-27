# Bitbucket Server Utilities

## Initial setup

1. Run `pip install -r requirements.txt`.
2. Set your script username and password via environment variables.  NOTE: If your password contains special characters,
they will most likely need to be escaped when adding them as environment variables.
    - On Windows via cmd (do NOT use Powershell):
    ```
        set SCRIPT_USERNAME=<username> (no quotes)
        set SCRIPT_PASSWORD=<password> (no quotes)
    ```
    - On MacOS/Linux or Windows via git-bash:
    ```
        export SCRIPT_USERNAME="<username>"
        export SCRIPT_PASSWORD="<password>"
    ```
3. Create a YAML file based on the supplied [example-run_batch.yml](example-run_batch.yml) or [example-generate_script.yml](example-generate_script.yml).
4. Modify the `bitbucket` and `jenkins` keys to suit your scenario.

## Execute batch operations on a Bitbucket project

1. Add project operations list items to the `project-operations` key.  Available project operations can be found in [run_batch.py](run_batch.py) by searching for `__project_ops__`.
2. Run `python run_batch.py -f <yaml-file>`

## Execute batch operations on repos in a Bitbucket project

1. Modify the `inclusions` or `exclusions` keys to suit your scenario.  If both inclusions and exclusions are provided, only the inclusions will be used.
2. Add operations list items to the `operations` key.  Available project operations can be found in [run_batch.py](run_batch.py) by searching for `__ops__`.
3. Run `python run_batch.py -f <yaml-file>`

## Generate a script to run against Bitbucket repos

1. Modify the `inclusions` or `exclusions` keys to suit your scenario.  If both inclusions and exclusions are provided, only the inclusions will be used.
2. Add a list item for each command to generate under the `commands` key.
3. Run:
    - Windows via cmd (do NOT use Powershell): `python generate_script.py -f <yaml-file> > script.bat`
    - MacOS/Linux or Windows via git-bash: `python generate_script.py -f <yaml-file> > script.sh && chmod +x script.sh`
4. Run the generated script:
    - Windows: `script.bat`
    - MacOS/Linux or Windows via git-bash: `./script.sh`