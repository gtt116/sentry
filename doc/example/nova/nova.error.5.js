{
  "_context_request_id": "req-f465ed94-02fa-49f0-81d0-bd17e79fd371", 
  "_context_quota_class": null, 
  "event_type": "remove_host_from_aggregate", 
  "_context_service_catalog": [
    {
      "endpoints_links": [], 
      "endpoints": [
        {
          "adminURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad", 
          "region": "RegionOne", 
          "publicURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad", 
          "id": "4eb84e99530a45928f021ad531be166f", 
          "internalURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad"
        }
      ], 
      "type": "volume", 
      "name": "cinder"
    }
  ], 
  "_context_auth_token": "35a54a1d239742f3a36b1fb93e74eb14", 
  "_context_user_id": "ebb67235828d40f6a4e0db00c6cc5a6f", 
  "payload": {
    "exception": {
      "kwargs": {
        "host": "nonexist_host_-tempest-1147658631", 
        "code": 404
      }
    }, 
    "args": {
      "self": null, 
      "host_name": "nonexist_host_-tempest-1147658631", 
      "context": {
        "project_name": "admin", 
        "user_id": "ebb67235828d40f6a4e0db00c6cc5a6f", 
        "roles": [
          "admin"
        ], 
        "_read_deleted": "no", 
        "timestamp": "2014-12-31T13:58:06.920415", 
        "auth_token": "35a54a1d239742f3a36b1fb93e74eb14", 
        "remote_address": "10.166.224.8", 
        "quota_class": null, 
        "is_admin": true, 
        "service_catalog": [
          {
            "endpoints": [
              {
                "adminURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad", 
                "region": "RegionOne", 
                "internalURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad", 
                "id": "4eb84e99530a45928f021ad531be166f", 
                "publicURL": "http://10.166.224.8:8776/v1/a2896e2e1b2b45a0bb2736e7f57d93ad"
              }
            ], 
            "endpoints_links": [], 
            "type": "volume", 
            "name": "cinder"
          }
        ], 
        "request_id": "req-f465ed94-02fa-49f0-81d0-bd17e79fd371", 
        "instance_lock_checked": false, 
        "project_id": "a2896e2e1b2b45a0bb2736e7f57d93ad", 
        "user_name": "admin"
      }, 
      "aggregate_id": "14"
    }
  }, 
  "priority": "ERROR", 
  "_context_is_admin": true, 
  "_context_user": "ebb67235828d40f6a4e0db00c6cc5a6f", 
  "publisher_id": "compute.netease-havana", 
  "message_id": "9898d200-9fe9-4377-8e5e-dbce939f96cb", 
  "_context_remote_address": "10.166.224.8", 
  "_context_roles": [
    "admin"
  ], 
  "timestamp": "2014-12-31 13:58:06.985379", 
  "_context_timestamp": "2014-12-31T13:58:06.920415", 
  "_unique_id": "a024371336174011b6bd9a0a193641e3", 
  "_context_project_name": "admin", 
  "_context_read_deleted": "no", 
  "_context_tenant": "a2896e2e1b2b45a0bb2736e7f57d93ad", 
  "_context_instance_lock_checked": false, 
  "_context_project_id": "a2896e2e1b2b45a0bb2736e7f57d93ad", 
  "_context_user_name": "admin"
}