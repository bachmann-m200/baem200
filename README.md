# baem200

Bachmann electronic Python Util Library

Connection und utils methods for M200 Serie

## Content

* **m1com**

Wrapper for the m1com.dll

* **m1config**

Python methods to read and write mconfig.ini files for the M200 controller

* **utils**

Some Python methods to set IP-Address and find M200 controller in the network

## Gettiing Started

Please install this library on you local computer

### Installation

```
pip install baem200
```

### Example

```
from baem200.m1com import PyCom, M1Controller
from pprint import pprint

dll = PyCom()
mh = M1Controller(dll, 'your_M1_IP')
mh.connect()
pprint(mh.getListofHwModules())
mh.disconnect()
```

## License

This project is licensed under Bachmann electronic License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* 
