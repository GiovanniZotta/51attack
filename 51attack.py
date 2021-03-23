network_hashrate= 168 * 10**18 # 168 EH/s
power = 51 # share of the hashrate the attacker wants to control
network_power = 100 - power
kwh_price = 0.01 # suppose 0.01$ for 1KWh (could be much less)
total_attacker_hashrate = (network_hashrate / network_power) * power
# the following number should take into account the "discount" that a large scale ASIC production has
cost_HS = 5000 / 10**(14) # cost of 1 H/S. Based on consumer price antminer s19j => rounded to 100TH/s for $5000(3KWh)
rewrite = 6 # number of blocks to rewrite


def get_reach_time():
    # suppose no difficulty readjustment, and that the honest chain mines 1 block every 10 minutes
    honest_block = rewrite
    malicious_block = 0
    hours = 0
    while(malicious_block < honest_block):
        # every hour
        hours += 1
        honest_block += 6
        malicious_block += 6 * (power / network_power)
        # print(f"Honest block: {honest_block}, Malicious block: {malicious_block}")

    return hours

def get_electricity_cost_per_hour():
    consumption_per_hour = 3 * total_attacker_hashrate / 10 ** (14) # (KWh) an ASIC that produces 100TH/s and consumes 3KWh
    # this looks pretty conservative, as it approximates at around 45TWh per year, while various sources report 80-120TWh per year (maybe because this ASIC is rather recent)
    # print(f"Consumption per hour: {consumption_per_hour/10**6} GWh")
    return consumption_per_hour * kwh_price 

def main():
    hardware_cost = total_attacker_hashrate * cost_HS
    print(f"Cost of hardware manufacturing: ${round(hardware_cost/10**6, 2)} M")
    electricity_cost_per_hour = get_electricity_cost_per_hour()
    print(f"Cost of electricity per hour: ${round(electricity_cost_per_hour, 2)}")
    hours = get_reach_time()
    print(f"The attacker needs {hours} hours to rewrite {rewrite} blocks, which would cost them ${round(hours * electricity_cost_per_hour, 2)}")

main()
