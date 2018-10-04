## To Protect your Infrastructure
Small app reads and parse your hcl   
Idea is to have an opensource sentinel like application for individual users and small companies, if you are looking for support or a full fledged platform please checkout hashicorp sentinel.

## required modules:
hcl: `pip install pyhcl`   
or   
`pip install -r requirements.txt`

## To test:
`python -m unittest discover tests/`

## structure

### allowed services:
To add a service in the allowed services you need to add it to the list in the
allowed.json file in the services directory

### policies
To add a policy you need to create a json file inside the policies directory
matching the service name (e.g. aws_s3_bucket.json) and must have following key-values:   
`tags` : A list for all the tags required to be there   
`exist`: A list for all the required attributes that must exist (e.g. versioning)   
`not-exist`: A list for all the attributes that should not exist (e.g. acl)   

## Contributing
To contribute to this opensource project please submit a pull request with your changes, all changes must be tested (we use python default unittest) and must be pep8 formatted.
