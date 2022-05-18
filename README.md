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

## Getting Started

Please install this library on you local computer

### Installation

```
pip install baem200
```

### Example

```
from baem200.m1com import M1Controller
from pprint import pprint

mh = M1Controller('your_M1_IP')
mh.connect()
pprint(mh.getListofHwModules())
mh.disconnect()
```

### Documentation
The full documentation can be found in the ['doc' directory](https://github.com/bachmann-m200/baem200/tree/master/doc). Here you can for example navigate to the 'html/index.html' file to find a full description of each method (content should be downloaded first).

Furthermore, the files ending with 'Test.py' show an example for each class and each method in the class ([example: m1comTest.py](https://github.com/bachmann-m200/baem200/blob/001e40ef145846639e368c378679d27c14709921/baem200/m1comTest.py#L199)

Below you can directly view the documentation of all the available classes in the browser:
[M1Controller](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_controller.html)
[M1Application](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_application.html)
[M1SVIObserver](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_s_v_i_observer.html)
[M1SVIReader](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_s_v_i_reader.html)
[M1SVIWriter](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_s_v_i_writer.html)
[M1TargetFinder](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1_m1_target_finder.html)
[\_M1SwModule](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1___m1_sw_module.html)
[\_SVIVariable](http://htmlpreview.github.io/?https://github.com/bachmann-m200/baem200/blob/master/doc/html/classbaem200_1_1baem200_1_1m1com_1_1___s_v_i_variable.html)
[PyCom](http://htmlpreview.github.io/?classbaem200_1_1baem200_1_1m1com_1_1_py_com.html)


## License

This project is licensed under Bachmann electronic License - see the [LICENCE](LICENCE) file for details

## Acknowledgments

* 
