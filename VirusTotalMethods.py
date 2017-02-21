import virustotal

API_KEY = "106b233ec0c0cd966f63c6e28fca35c36e1f916e1ccc3838e9dc2f21f5ed9ae0"


def scan_file(file_path):
    v = virustotal.VirusTotal(API_KEY)
    report = v.scan(file_path)
    report.join()
    assert report.done == True
    return report
