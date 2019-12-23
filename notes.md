# Sony Device Control

## Overview

Investigation is being performed on a Sony UBP-X700 (Blu-ray Disc Player). Follow up work will be done on the Bravia TVs
in my house.

### Goal

The purpose of this library is to allow for controlling a Sony device (from here on referred to as a "device")
by registering a "controller", and then sending authenticated requests over HTTP.

Control of Sony devices using a generic API, to control as much as possible using the services/protocols provided by
Sony.

The difficulty lies in the fact that Sony seems to change the endpoints from time to time, but this should hopefully be
handled by reading the correct static endpoints to get the locations of the services required.

## Ports

```
nmap -Pn 192.168.1.138 -p 1-65535
Starting Nmap 7.80 ( https://nmap.org ) at 2019-11-07 21:22 GMT
Nmap scan report for udhcp-0-9-9-pre-44-e4-ee-04-d4-18.lan (192.168.1.138)
Host is up (0.021s latency).
Not shown: 65528 closed ports
PORT      STATE SERVICE
9090/tcp  open  zeus-admin
50001/tcp open  unknown
50002/tcp open  iiimsf
50201/tcp open  unknown
50202/tcp open  unknown
52323/tcp open  unknown
54400/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 495.47 seconds
```

### Tools

* Wireshark
* Video & Video SideView (Android)
* Packet Capture (Android)

## Discovery

Device information can be found here: GET http://192.168.1.138:50001/Ircc.xml

Returns something like this:

```xml
<?xml version="1.0"?>
<root xmlns="urn:schemas-upnp-org:device-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  <device>
    <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>
    <friendlyName>UBP-X700</friendlyName>
    <manufacturer>Sony Corporation</manufacturer>
    <manufacturerURL>http://www.sony.net/</manufacturerURL>
    <modelDescription></modelDescription>
    <modelName>Blu-ray Disc Player</modelName>
    <modelURL></modelURL>
    <UDN>uuid:00000003-0000-1010-8000-44e4ee04d418</UDN>
    <iconList>
      <icon>
        <mimetype>image/jpeg</mimetype>
        <width>120</width>
        <height>120</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_large.jpg</url>
      </icon>
      <icon>
        <mimetype>image/png</mimetype>
        <width>120</width>
        <height>120</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_large.png</url>
      </icon>
      <icon>
        <mimetype>image/jpeg</mimetype>
        <width>48</width>
        <height>48</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_small.jpg</url>
      </icon>
      <icon>
        <mimetype>image/png</mimetype>
        <width>48</width>
        <height>48</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_small.png</url>
      </icon>
    </iconList>
    <serviceList>
      <service>
        <serviceType>urn:schemas-sony-com:service:IRCC:1</serviceType>
        <serviceId>urn:schemas-sony-com:serviceId:IRCC</serviceId>
        <SCPDURL>/IRCCSCPD.xml</SCPDURL>
        <controlURL>/upnp/control/IRCC</controlURL>
        <eventSubURL></eventSubURL>
      </service>
    </serviceList>
    <presentationURL></presentationURL>
    <av:X_IRCC_DeviceInfo xmlns:av="urn:schemas-sony-com:av">
      <av:X_IRCC_Version>1.0</av:X_IRCC_Version>
      <av:X_IRCC_CategoryList>
        <av:X_IRCC_Category>
          <av:X_CategoryInfo>AAMAABxa</av:X_CategoryInfo>
        </av:X_IRCC_Category>
      </av:X_IRCC_CategoryList>
    </av:X_IRCC_DeviceInfo>
    <av:X_UNR_DeviceInfo xmlns:av="urn:schemas-sony-com:av">
      <av:X_UNR_Version>1.3</av:X_UNR_Version>
      <av:X_CERS_ActionList_URL>http://192.168.1.138:50002/actionList</av:X_CERS_ActionList_URL>
    </av:X_UNR_DeviceInfo>
    <av:X_RDIS_DeviceInfo xmlns:av="urn:schemas-sony-com:av">
      <av:X_RDIS_Version>1.0</av:X_RDIS_Version>
      <av:X_RDIS_SESSION_CONTROL>false</av:X_RDIS_SESSION_CONTROL>
      <av:X_RDIS_ENTRY_PORT>50004</av:X_RDIS_ENTRY_PORT>
    </av:X_RDIS_DeviceInfo>
  </device>
</root>
```

So we can get the device model, icons and a list of services available.

## UPnP

More device information can be found here: http://192.168.1.138:52323/dmr.xml

```xml
<?xml version="1.0"?>
<root xmlns="urn:schemas-upnp-org:device-1-0" xmlns:pnpx="http://schemas.microsoft.com/windows/pnpx/2005/11" xmlns:df="http://schemas.microsoft.com/windows/2008/09/devicefoundation" xmlns:av="urn:schemas-sony-com:av">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  <device>
    <deviceType>urn:schemas-upnp-org:device:MediaRenderer:1</deviceType>
    <friendlyName>UBP-X700</friendlyName>
    <manufacturer>Sony Corporation</manufacturer>
    <manufacturerURL>http://www.sony.net/</manufacturerURL>
    <modelName>UBP-X700</modelName>
    <modelNumber>BDP-2018</modelNumber>
    <UDN>uuid:00000000-0000-1010-8000-cc988be59ecc</UDN>
    <dlna:X_DLNADOC xmlns:dlna="urn:schemas-dlna-org:device-1-0">DMR-1.50</dlna:X_DLNADOC>
    <dlna:X_DLNACAP xmlns:dlna="urn:schemas-dlna-org:device-1-0">playcontainer-0-0</dlna:X_DLNACAP>
    <iconList>
      <icon>
        <mimetype>image/jpeg</mimetype>
        <width>120</width>
        <height>120</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_large.jpg</url>
      </icon>
      <icon>
        <mimetype>image/png</mimetype>
        <width>120</width>
        <height>120</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_large.png</url>
      </icon>
      <icon>
        <mimetype>image/jpeg</mimetype>
        <width>48</width>
        <height>48</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_small.jpg</url>
      </icon>
      <icon>
        <mimetype>image/png</mimetype>
        <width>48</width>
        <height>48</height>
        <depth>24</depth>
        <url>/bdp_ce_device_icon_small.png</url>
      </icon>
    </iconList>
    <serviceList>
      <service>
        <serviceType>urn:schemas-upnp-org:service:RenderingControl:1</serviceType>
        <serviceId>urn:upnp-org:serviceId:RenderingControl</serviceId>
        <SCPDURL>/RenderingControlBdpSCPD.xml</SCPDURL>
        <controlURL>/upnp/control/RenderingControl</controlURL>
        <eventSubURL>/upnp/event/RenderingControl</eventSubURL>
      </service>
      <service>
        <serviceType>urn:schemas-upnp-org:service:ConnectionManager:1</serviceType>
        <serviceId>urn:upnp-org:serviceId:ConnectionManager</serviceId>
        <SCPDURL>/ConnectionManagerSCPD.xml</SCPDURL>
        <controlURL>/upnp/control/ConnectionManager</controlURL>
        <eventSubURL>/upnp/event/ConnectionManager</eventSubURL>
      </service>
      <service>
        <serviceType>urn:schemas-upnp-org:service:AVTransport:1</serviceType>
        <serviceId>urn:upnp-org:serviceId:AVTransport</serviceId>
        <SCPDURL>/AVTransportBdpSCPD.xml</SCPDURL>
        <controlURL>/upnp/control/AVTransport</controlURL>
        <eventSubURL>/upnp/event/AVTransport</eventSubURL>
      </service>
    </serviceList>
    <av:X_StandardDMR>1.1</av:X_StandardDMR>
    <microsoft:magicPacketWakeSupported xmlns:microsoft="urn:schemas-microsoft-com:WMPNSS-1-0">
        1
    </microsoft:magicPacketWakeSupported>
  </device>
</root>
```

## Action list

Found during discovery: GET http://192.168.1.138:50002/actionList

Returns something like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<actionList>
  <action name="register" mode="3" url="http://192.168.1.138:50002/register"/>
  <action name="getText" url="http://192.168.1.138:50002/getText"/>
  <action name="sendText" url="http://192.168.1.138:50002/sendText"/>
  <action name="getContentInformation" url="http://192.168.1.138:50002/getContentInformation"/>
  <action name="getSystemInformation" url="http://192.168.1.138:50002/getSystemInformation"/>
  <action name="getRemoteCommandList" url="http://192.168.1.138:50002/getRemoteCommandList"/>
  <action name="getStatus" url="http://192.168.1.138:50002/getStatus"/>
  <action name="getHistoryList" url="http://192.168.1.138:50002/getHistoryList"/>
</actionList>
```

This gives us a list of endpoints we can use to register a controller and get system info. We should build all of there endpoints into a single module.

### Register

Documentation found online: GET http://192.168.1.138:50002/register

This endpoint is used to register a controller. The following params need to be added to the endpoint:

- deviceName: Display name for the device to show in the menu
- deviceId: A unique identifier for the controller
- registrationType: Should be set to initial. Seems to be fine to leave in the request when entering the PIN

The first of these requests should prompt the device to display a PIN, which can be sent to the device using the same endpoint, but adding the PIN as a Basic auth token header with the request

Once registered, the rest of the endpoints are authenticated by adding the following headers:

- X-CERS-DEVICE-INFO: The device name used during registration
- X-CERS-DEVICE-ID: The device id used during registration

## UPnP/SCDP

Found during discovery (though I didn't know the port, that came from online): GET http://192.168.1.138:52323/IRCCSCPD.xml

```xml
<?xml version="1.0"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  
  <actionList>
    <action>
      <name>X_SendIRCC</name>
      <argumentList>
        <argument>
          <name>IRCCCode</name>
          <direction>in</direction>
          <relatedStateVariable>X_A_ARG_TYPE_IRCCCode</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
        
    <action>
      <name>X_GetStatus</name>
      <argumentList>
        <argument>
          <name>CategoryCode</name>
          <direction>in</direction>
          <relatedStateVariable>X_A_ARG_TYPE_Category</relatedStateVariable>
        </argument>
        <argument>
          <name>CurrentStatus</name>
          <direction>out</direction>
          <relatedStateVariable>X_A_ARG_TYPE_CurrentStatus</relatedStateVariable>
        </argument>
        <argument>
          <name>CurrentCommandInfo</name>
          <direction>out</direction>
          <relatedStateVariable>X_A_ARG_TYPE_CurrentCommandInfo</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  
  <serviceStateTable>
    <stateVariable sendEvents="no">
      <name>X_A_ARG_TYPE_IRCCCode</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>X_A_ARG_TYPE_Category</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>X_A_ARG_TYPE_CurrentStatus</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>X_A_ARG_TYPE_CurrentCommandInfo</name>
      <dataType>string</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>

```

Something to do with SCPD (Service Control Point Definition), need to dig into this more (there may be a library that handles this stuff, or maybe we just ignore it):

## IRCC

Found during discovery: POST http://192.168.1.138:50001/upnp/control/IRCC

This does not follow the IRCC-IP documentation exactly (the URI and port are different), but does seem to use the same message formats.

The correct endpoint and port can be found in Ircc.xml

Headers:
```
Content-Length: 317
Content-Type: text/xml; charset=UTF-8
SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"
```

Body
```xml
<?xml version="1.0"?>\n
<s:Envelope xmlns:s="[Link: schemas.xmlsoap.org] /encoding/">
  <s:Body>
    <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
      <IRCCCode>AAAAAwAAHFoAAAAaAw==</IRCCCode>
    </u:X_SendIRCC>
  </s:Body>
</s:Envelope>
```
