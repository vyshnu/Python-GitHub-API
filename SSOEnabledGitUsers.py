import requests
import json
import sys
import config

class GitHubGraphQLQuery(object):

    BASE_URL = "https://api.github.com/graphql"

    def __init__(self, token, query, variables=None, additional_headers=None):
        self._token = token
        self._query = query
        self._variables = variables or dict()
        self._additional_headers = additional_headers or dict()

    @property
    def headers(self):
        default_headers = dict(Authorization="token {}".format(self._token))
        return dict(default_headers.items() + self._additional_headers.items())

    def generator(self):
        while True:
            try:
                yield requests.request(
                    "post",
                    GitHubGraphQLQuery.BASE_URL,
                    headers={"Authorization": "Bearer {0}".format(pt)},
                    json={"query": self._query, "variables": self._variables},
                ).json()
            except requests.exceptions.HTTPError as http_err:
                raise http_err
            except Exception as err:
                raise err

    def iterator(self):
        pass

class GithubSAMLIdentityProvider(GitHubGraphQLQuery):

    QUERY = """
        query($org: String!, $after: String) {
            organization(login: $org) {
                samlIdentityProvider {
                    ssoUrl,
                    externalIdentities(first: 100, after: $after) {
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        edges {
                            node {
                                guid,
                                samlIdentity {
                                    nameId
                                }
                                user {
                                    login
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    ADDITIONAL_HEADERS = dict(Accept="application/vnd.github.vixen-preview+json")

    def __init__(self, organization_name, token):
        super(GithubSAMLIdentityProvider, self).__init__(
            token=token,
            query=GithubSAMLIdentityProvider.QUERY,
            variables=dict(org=organization_name, after=None),
            additional_headers=GithubSAMLIdentityProvider.ADDITIONAL_HEADERS,
        )
        self._identities = list()

    def iterator(self):
        generator = self.generator()
        hasNextPage = True
        saml_identities = list()
        while hasNextPage:
            response = next(generator)
            endCursor = response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["pageInfo"]["endCursor"]
            self._variables["after"] = endCursor
            saml_identities.extend(
                response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["edges"]
            )
            hasNextPage = response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["pageInfo"]["hasNextPage"]
        return saml_identities

org="mygithuborg" #Add your GitHuborg here
pt=config.getpattoken()
sys.stdout = open("sso_output.csv", "w")
#Print the headers
print("{0},{1}".format("email","login"))
GHSIP = GithubSAMLIdentityProvider(org,pt)
mailList = GHSIP.iterator()
for val in mailList:
    #print(mail)
    try:
        email = (val["node"]["samlIdentity"]["nameId"])
        login=(val["node"]["user"]["login"])
    except IndexError:
        email = 'null'
    except TypeError: 
        userId = 'null' 
    print("{0},{1}".format(email, login))

sys.stdout.close()
© 2021 GitHub, Inc.
