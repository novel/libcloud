import httplib
import os.path
import sys
import unittest

from libcloud.resource.lb.drivers.rackspace import RackspaceLBDriver

from test import MockHttp, MockRawResponse
from test.file_fixtures import ResourceFileFixtures

class CloudFilesTests(unittest.TestCase):

    def setUp(self):
        RackspaceLBDriver.connectionCls.conn_classes = (None,
                RackspaceLBMockHttp)
        RackspaceLBMockHttp.type = None
        self.driver = RackspaceLBDriver('user', 'key')

    def test_list_balancers(self):
        balancers = self.driver.list_balancers()

        self.assertEquals(len(balancers), 2)
        self.assertEquals(balancers[0].name, "test0")
        self.assertEquals(balancers[0].id, "8155")
        self.assertEquals(balancers[1].name, "test1")
        self.assertEquals(balancers[1].id, "8156")

class RackspaceLBMockHttp(MockHttp):
    fixtures = ResourceFileFixtures(os.path.join('lb', 'rackspace'))

    def _v1_0(self, method, url, body, headers):
        headers = {'x-server-management-url': 'https://servers.api.rackspacecloud.com/v1.0/slug',
                   'x-auth-token': 'FE011C19-CF86-4F87-BE5D-9229145D7A06',
                   'x-cdn-management-url': 'https://cdn.clouddrive.com/v1/MossoCloudFS_FE011C19-CF86-4F87-BE5D-9229145D7A06',
                   'x-storage-token': 'FE011C19-CF86-4F87-BE5D-9229145D7A06',
                   'x-storage-url': 'https://storage4.clouddrive.com/v1/MossoCloudFS_FE011C19-CF86-4F87-BE5D-9229145D7A06'}
        return (httplib.NO_CONTENT, "", headers, httplib.responses[httplib.NO_CONTENT])

    def _v1_0_slug_loadbalancers(self, method, url, body, headers):
        body = self.fixtures.load('v1_slug_loadbalancers.json')
        return (httplib.OK, body, {}, httplib.responses[httplib.OK])

if __name__ == "__main__":
    sys.exit(unittest.main())
