import ipaddress


def is_ipv6_in_range(ip, start, end):
    ip = ipaddress.IPv6Address(ip)
    start = ipaddress.IPv6Address(start)
    end = ipaddress.IPv6Address(end)
    return start <= ip <= end


# 使用示例
start = "2001:0db8:85a3:08d3:1319:8a2e:0370:7334"
end = "2001:0db8:85a3:08d3:1319:8a2e:0370:9999"

test_ip = "2001:0db8:85a3:08d3:1319:8a2e:0370:8000"
result = is_ipv6_in_range(test_ip, start, end)
print(f"IP {test_ip} 在指定范围内: {result}")
