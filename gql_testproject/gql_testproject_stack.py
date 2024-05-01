from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_appsync as appsync,
    
    # aws_sqs as sqs,
)
from aws_cdk import CfnOutput
from constructs import Construct

class GqlTestprojectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        '''steps for using AWS Lambda as datasource in GraphQl API
        
        setp1. Define a GraphQl Schema as defined in graphqlschema.gql file 
        setp2. Create a GraphQl API using AWS AppSync using schema created in step#1. For security purpose use API_KEY. There are many other
            options to prevent unauthorized access like AWS Ampliy, IAM etc. But for simplicity we are using
            APIKEY
        set3. Create Lambda function
        step3. Create/Add Lambda we created in step#3 as GraphQl DataSource. Here we have to specify the lambda
                function which will be used as Datasource
        step4. Create Resolver for each Query field
        setp5. Go to aws console and head over the AppSync. on left hand sidebar there is option for 'setting',
                click on it and get GraphQL endpoint and scroll down there will be and APIKEY in 'Primay auth mode'
                section.
        setp6. copy Graphql endpoint and api key. open Postman set Post method and insert GraphQl endpoint and from body
                select GraphQL. in Header section, set two keys value pairs
                    1.x-api-key====> <APIKEY copied>
                    2.Content-Type====> application/graphql
        step7. Write qurey

        '''
        hLambda=self.createLambda('demolambda','./resources','HWlambda.lambda_handler')
        hLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        gqpapi=self.createGQLApi('testgqlApi','demoapi','./graphql/graphqlschema.gql')

        # Print Graphql Api Url on console after deploy
       # CfnOutput(self,"APIGraphQlURL",value=gqpapi.graphqlUrl)
       # CfnOutput(self, "GraphQlApiKey", value=gqpapi.apikey or "")
       
        #set lambda as DataSource
        lambdadatasource=gqpapi.add_lambda_data_source("MyLambdaDataSource",
                                                        name="MyLambdaDataSource",
                                                        description="My Lambda DataSource",
                                                        lambda_function=hLambda
                                )
        # resolvers
        lambdadatasource.create_resolver("testResolver1",
        type_name="Query",
        field_name="notes"
        )
        lambdadatasource.create_resolver("testResolver2",
        type_name="Query",
        field_name="customNote"
        )



 # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_appsync/README.html
    def createGQLApi(self,id,name,schema):
        api = appsync.GraphqlApi(self,id ,
        name=name,
        definition=appsync.Definition.from_file(schema),
        
        authorization_config=appsync.AuthorizationConfig(
            default_authorization=appsync.AuthorizationMode(
                authorization_type=appsync.AuthorizationType.API_KEY,
            )
        )
        ) 
        return api   

# https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html
    def createLambda(self,id,resources,handler):
        return lambda_.Function(self, id,
        code=lambda_.Code.from_asset(resources),
        handler=handler,
        runtime=lambda_.Runtime.PYTHON_3_9
        
    )