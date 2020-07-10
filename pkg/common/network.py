from utils.dbconn import *
from utils.converter import *
from model.discover import *
from model.blueprint import *


def update_nw_cidr():
    con = create_db_con()
    machines = json.loads(Discover.objects.to_json())
    networks = []
    for machine in machines:
      networks.append(machine['network'])
    network_count = len(list(set(networks)))
    networks = list(set(networks))
    vpc_cidr = defaultdict(list)
    subnet_machines = defaultdict(list)
    vpcs = defaultdict(list)
    for i in machines:
      vpc_cidr[i['network']].append(i['subnet'])
    for i in vpc_cidr.keys():
      subnet_prefixes = []
      subnet_prefix = 0
      for j in vpc_cidr[i]:
        subnet_prefixes.append(int(j.split('/')[-1]))
        subnet_prefix = min(subnet_prefixes)
        vp = i+'/'+str(subnet_prefix-2)
        if '/' not in i:
          Discover.objects(network=i).update(network=vp)
          con.close()
          return true
    con.close()
    return false
    
def update_subnet():
    con = create_db_con()
    machines = json.loads(Discover.objects.to_json())
    if cidr == '10.0.0.0':
      for machine in machines:
        if machine['network'].split('.')[0] == '10':
          continue
        machine['ip'] = machine['ip'].split('.')
        machine['ip'][0] = '10'
        machine['ip'] = '.'.join(machine['ip'])
        machine['network'] = machine['network'].split('.')
        machine['network'][0] = '10'
        machine['network'] = '.'.join(machine['network'])
        machine['subnet'] = machine['subnet'].split('.')
        machine['subnet'][0] = '10'
        machine['subnet'] = '.'.join(machine['subnet'])
       # print machine
    elif cidr == '172.16.0.0':
      for machine in machines:
        if machine['network'].split('.')[0] == '172':
          continue
        machine['ip'] = machine['ip'].split('.')
        machine['ip'][0] = '172'
        machine['ip'][1] = '16'
        machine['ip'] = '.'.join(machine['ip'])
        machine['network'] = machine['network'].split('.')
        machine['network'][0] = '172'
        machine['network'][1] = '16'
        machine['network'] = '.'.join(machine['network'])
        machine['subnet'] = machine['subnet'].split('.')
        machine['subnet'][0] = '172'
        machine['subnet'][1] = '16'
        machine['subnet'] = '.'.join(machine['subnet'])
        #print machine
    elif cidr == '192.168.0.0':
      for machine in machines:
        if machine['network'].split('.')[0] == '192':
          continue
        machine['ip'] = machine['ip'].split('.')
        machine['ip'][0] = '192'
        machine['ip'][1] = '168'
        machine['ip'] = '.'.join(machine['ip'])
        machine['network'] = machine['network'].split('.')
        machine['network'][0] = '192'
        machine['network'][1] = '168'
        machine['network'] = '.'.join(machine['network'])
        machine['subnet'] = machine['subnet'].split('.')
        machine['subnet'][0] = '192'
        machine['subnet'][1] = '168'
        machine['subnet'] = '.'.join(machine['subnet'])
        #print machine
    con.close()
    return machines

def update_blueprint(machines):
    con = create_db_con()
    for machine in machines:
      ram = conv_KB(machine['ram'].split(' ')[0])
      machine['machine_type'] = compu(machine_type,int(machine['cores']),ram)
      post = BluePrint(host=machine['host'], ip=machine['ip'], subnet=machine['subnet'], network=machine['network'],
                 ports=machine['ports'], cores=machine['cores'], public_route=True, cpu_model=machine['cpu_model'], ram=machine['ram'],machine_type='',status='Not started')
      try:
        post.save()
      except Exception as e:
        print("Boss you have to see this!!")
        print(e)
      finally:
        con.close()
    return True

def create_nw_layout():
    con = create_db_con()
    try:
      BluePrint.objects.delete()
    except Exception as e:
      print("See the error:"+ str(e))
    network_cidr_updated = update_nw_cidr()
    if network_cidr_updated:
        machines = update_subnet()
        blueprint_updated = update_blueprint(machines)
    return blueprint_updated
