from pathlib import Path

from aclpath import ACLInfoRetriever

test_path = Path(__file__).parent
my_get_facl_result = ACLInfoRetriever(test_path).getfacl()

my_acl_data = my_get_facl_result.acl_data

print(my_acl_data)