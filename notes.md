# Sony Device Control

## Overview

The purpose of this library is to allow for controlling a Sony device (from here on referred to as a "device") by registering a "controller", and then sending authenticated requests over HTTP.

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

Found during discovery: POST http://192.168.1.138:52323/upnp/control/IRCC

This does not follow the IRCC-IP documentation exactly (the URI and port are different), but does seem to use the same message formats

I'm yet to send a successful message to this endpoint yet. Should hopefully be something like this:

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
