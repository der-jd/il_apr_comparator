# il-apr-comparator

[![CircleCI](https://circleci.com/gh/der-jd/il_apr_comparator.svg?style=shield&circle-token=8d10a608bd794e76c975b0bdedae7e1600c81cdc)](https://circleci.com/gh/der-jd/il_apr_comparator)

This tool gets the annual percentage rates (APRs) of the crypto currency liquidity mining pools from `Bake` (https://app.bake.io/liquidity-mining). Then it calculates for a given period of time the impermanent losses (ILs) of these pools and compares them with the according APRs. In the end it sends a notification to subscribers informing about the differences between IL and APR and the resulting yield.


## Architecture and application specifics

- The application is written with `Python`
- It is running via a `Docker` container inside an `AWS Lambda function`
- The Docker images are saved in an `AWS Elastic Container Registry (ECR)` repository
- The Lambda function is triggered on a schedule defined in `AWS EventBridge`
- Notifications are sent via `AWS Simple Notification Service (SNS)` to all subscribers
- To get notifications one has to manually add a subscription to the according SNS topic via the AWS console
- Necessary parameters are stored in the `Parameter Store` of the `AWS Systems Manager`
- To get the information about the liquidity mining pools the website of `Bake` (https://app.bake.io/liquidity-mining) is scraped on two different ways:
  - Classic HTML scraping when running the application locally
  - AI based scraping with the external service https://www.browse.ai/ when running inside the Lambda function or when running locally
- One needs to create an account for the `browse.ai` service and set up a robot to extract the necessary data from the Bake website
- The corresponding `API Key` and `Robot ID` from `browse.ai` are used to access the robot from the application
- The extracted data from the robot must match the following form:
  - Name of the table: `Coin_Pairs_LM_APR `
  - | Position | coin_pair | apr |
    |---|---|---|
    | 1 | BTC-DFI | XX% |
    | 2 | ETH-DFI | XX% |
    | ... | ... | ... |
- The data for the coin prices is taken from the public API of `CoinGecko` (https://www.coingecko.com/)
- Impermanent Loss is calculated based on the `Uniswap's constant product formula`. A simple online calculator can be found here: https://dailydefi.org/tools/impermanent-loss-calculator/

### Update dependencies for Python

- Install `pipreqs` Python package:
  - `pip install pipreqs`
- Create `requirements.txt`. Use `--force` to override already existent file:
  - `pipreqs --force <path_to_source_folder>`
- Manually (re)add any necessary dependencies removed by `pipreqs` (e.g. `lxml`)


## Build and deployment process

The whole build and deployment process is automated via `CircleCI` pipelines using `Continuous Integration (CI)` and `Continuous Deployment (CD)`.

### Necessary variables in CircleCI

#### Project environment variables

- AWS_ACCESS_KEY
- AWS_ACCOUNT_ID
- AWS_REGION
- AWS_ROLE_ARN
- AWS_SECRET_KEY

#### Contexts

- Context named `github` with a variable called `GH_PAT_CFN_SCRIPTS_REPO` (Personal Access Token for the GitHub repo containing the CloudFormation deployment scripts)
