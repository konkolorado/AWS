import simplejson, boto, uuid, time

"""
scp file from local server to cloud:
    set secutiry group rules inbound/outbound ssh-tcp-22-local_IP
    scp -i ~/.ssh/ec2-sample-key.pem datasets.py \
        ec2-user@ec2-54-172-177-58.compute-1.amazonaws.com:
"""

def upload_to_s3_example():
    # NOTE names can't have '.' in them
    # NOTE need to $export AWS_CREDENTIAL_FILE="~/.cred_file"
    bucketname = "mybucket"
    keyname = "mykey"
    localfile = "~/test.csv"
    upload_s3(bucketname, keyname, localfile)

def upload_s3(b_name, k_name, loc_file):
    s3 = boto.connect_s3() 
    bucket = s3.create_bucket(b_name)
    key = bucket.new_key(k_name)
    key.set_contents_from_filename(loc_file)
    key.set_acl('public-read')

def rename_data_s3_example():
    oldbucketname = "mybucket"
    oldkeyname = "mykey"
    newbucketname = "mybucket2"
    newkeyname = "mykey2"
    
    rename_s3(oldbucketname, oldkeyname, newbucketname, newkeyname)

def rename_s3(b_old, k_old, b_new, k_new):
    s3 = boto.connect_s3()
    s3.create_bucket(b_new)

    key = s3.get_bucket(b_old)
    key = key.get_key(k_old)

    new_key = key.copy(b_new, k_new, preserve_acl=True)
    if new_key.exists:
        key.delete()

def boot_instance_ec2_example():
    # NOTE
    # Make sure to know which image ID you need
    new_keypair_name = 'ec2-sample-key'
    new_keypair_dest = '/Users/urielmandujano/.ssh'
    image_id = 'ami-bb709dd2'

    boot_image(new_keypair_name, new_keypair_dest, image_id)


def boot_image(keypair_name, keypair_dest, ami_id):
    # only needs to be done once
    ec2 = boto.connect_ec2()
    key_pair = ec2.create_key_pair(keypair_name)
    key_pair.save(keypair_dest)

    reservation = ec2.run_instances(image_id=ami_id, key_name=keypair_name)
    time.sleep(120)
    for r in ec2.get_all_instances():
        if r.id == reservation.id:
            break
    print r.instances[0].public_dns_name

def main():
    upload_to_s3_example()
    rename_data_s3_example()
    boot_instance_ec2_example()


if __name__ == '__main__':
    main()
