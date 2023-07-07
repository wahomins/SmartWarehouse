/*
    Secure Credentials
*/

#ifndef SECRET
#define SECRET

#define MAJOR_VER "00"
#define MINOR_VER "00"

#define THINGNAME "QRCodeReader";

const char *STASSID = "KHAN";
const char *STAPSK = "Qwertyu80p";

int8_t TIME_ZONE = +3; //Nairobi(Kenya): +3 UTC

const char* MQTT_SERVER = "142.93.52.78";
const int MQTT_PORT = 1883;
const char* MQTT_USER = "mosquitto";
const char* MQTT_PASS = "mosquitto";
const char DEVICE_ID[] = "647f1b886210db7cb5a2d656";
char TOPIC_TO_HOST[] = "TO_HOST/Inventory/QR/";
char TOPIC_FROM_HOST[] = "TO_DEVICE/Inventory/QR/";
char TOPIC_CLIENT_CONNECTION[] = "CLIENT_CONNECTIONS/activity/";

char topic_to_host[sizeof(TOPIC_TO_HOST) + sizeof(DEVICE_ID)];
char topic_from_host[sizeof(TOPIC_FROM_HOST) + sizeof(DEVICE_ID)];
char topic_client_connection[sizeof(TOPIC_CLIENT_CONNECTION) + sizeof(DEVICE_ID)];

void setupConfig() {
  // Concatenate the DEVICE_ID with the topic strings
  strcpy(topic_to_host, TOPIC_TO_HOST);
  strcat(topic_to_host, DEVICE_ID);
  
  strcpy(topic_from_host, TOPIC_FROM_HOST);
  strcat(topic_from_host, DEVICE_ID);
  
  strcpy(topic_client_connection, TOPIC_CLIENT_CONNECTION);
  strcat(topic_client_connection, DEVICE_ID);
  
  // Rest of your setup code...
  Serial.println(topic_to_host);
  Serial.println(topic_from_host);
  Serial.println(topic_client_connection);
}


const char CA_CERT_PROG[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDtTCCAp2gAwIBAgIUB1bEK+0djl3XTfYbo7QKLYhV//swDQYJKoZIhvcNAQEL
BQAwajELMAkGA1UEBhMCS0UxEDAOBgNVBAgMB05haXJvYmkxEDAOBgNVBAcMB05h
aXJvYmkxEjAQBgNVBAoMCVNhZmFyaWNvbTELMAkGA1UECwwCQ0ExFjAUBgNVBAMM
DTE5Mi4xNjguMTAwLjUwHhcNMjMwNjA4MDUxNzM2WhcNMjQwNjA3MDUxNzM2WjBq
MQswCQYDVQQGEwJLRTEQMA4GA1UECAwHTmFpcm9iaTEQMA4GA1UEBwwHTmFpcm9i
aTESMBAGA1UECgwJU2FmYXJpY29tMQswCQYDVQQLDAJDQTEWMBQGA1UEAwwNMTky
LjE2OC4xMDAuNTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJZTEdWT
WvSExeGIbSXs5wWIcGRHKOUdt/XYWSF8iLnuSg6MTAJ92fu+rorAtf1+6rD8ILCP
U77U9yqw64Hf6k6w+GmtoBIWYm54QBh05m/ktaD1ck9QPn4LKmFcdJvy3O5TsrfK
jGo75EbYB54IhTZHy0T/DeeCMuXRBY8FFcUAysAd6Z2GsUdRdQzns3AfLvsOFYIw
UxwbijbPBQFsQWPsoDdcfwBUmOpeO/y0QZHc94ffc6crf4RTESQ/lXSqE3ykbB2/
kE/TPeh2D5a1TmzGQsOEKNz3BMl99XhgIjaSZ6dP0LZtZW3E2SvdY+bnTveJ4L7s
PkFERcHVIpb8zzMCAwEAAaNTMFEwHQYDVR0OBBYEFEmaO8sxcE4ywHzjVkPNIKHP
TTmSMB8GA1UdIwQYMBaAFEmaO8sxcE4ywHzjVkPNIKHPTTmSMA8GA1UdEwEB/wQF
MAMBAf8wDQYJKoZIhvcNAQELBQADggEBADL36S/p5+hQoyHjh7vdC3DVu5uZD5/J
0VOOIohbPmcmGh1ooAMPvfSIXgRZUcTnNGwvf9NUZ5BXGbCRkjAgAfswlb1tS5LX
ZQeFsvQWgzfAXzlkEAONA6D2TO1DJ0bYt7z0ex5xDfVnAdnspmkw63o1m7SKr8Nc
wow+wfVNLvtijBiQi76eQU1iT8qn6cTAMbvsaiPltKPRo+3teF1VDE56l+j9oFuK
y5zFxzGJA4W5gmPAUz6VgGktrLzbyptvP+/PDNt57ydsxqwSFl0uWRmiT+MgyQT9
FINWVEec6gc040qobwolCdZKsM+iHg0YYHOUGRtS8TjMKOHQpsmrxuw=
-----END CERTIFICATE-----
)EOF";

const char CLIENT_CERT_PROG[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDXzCCAkcCFEv0m/n/Tse43m5v8mLvz6bHUyAzMA0GCSqGSIb3DQEBCwUAMGox
CzAJBgNVBAYTAktFMRAwDgYDVQQIDAdOYWlyb2JpMRAwDgYDVQQHDAdOYWlyb2Jp
MRIwEAYDVQQKDAlTYWZhcmljb20xCzAJBgNVBAsMAkNBMRYwFAYDVQQDDA0xOTIu
MTY4LjEwMC41MB4XDTIzMDYwODA1MTczN1oXDTI0MDYwNzA1MTczN1owbjELMAkG
A1UEBhMCS0UxEDAOBgNVBAgMB05haXJvYmkxEDAOBgNVBAcMB05haXJvYmkxEjAQ
BgNVBAoMCVNhZmFyaWNvbTEPMA0GA1UECwwGQ2xpZW50MRYwFAYDVQQDDA0xOTIu
MTY4LjEwMC41MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArJ86U4x9
GGsOjGkLASMekyWxIsLtdlxH3zLiDMCJGLqWmo+WbN1s924cKDlaa59ZAaG5Q0+9
SNEUOmjB57NyVCoIrdu+Cjtl+8Pbj4QsoKjxO+EASa+T7WW9EkbMia4Cl5qXj/fQ
Hx8QmbBv55QEWnQAEj/cLNN1WR0AvwGilZvu5JiEX3BEO1L3SkF86AEz/8OnRLng
+a7b3G7IYxKfKOSSFnPQ3Tvfk8P9YmkrXMgI0nANM1aV9lDH/WIPZJhWCPfb7uTM
jgDCreoGo0nBWnHXxLSWZhH46UVGa7Hmenpqt7QAI6lRNN9GkQRoVmTG65nUky/y
al8aJkXAFRXU4wIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQB4PE7SpGf24/14bLbL
1PhD9xuzxZwwCaBJsbysD7SERtz/rKmBGQ9rZzGG1dHUEk1EvUN8bTbRHiIEfLuO
LJDCnYT9gTtA8BtLxHHKImB3tPgltNc5/Ge5nTgeuksb8qsoCbqQL4+qrBiyvZGG
+EPn/BHjVUlXR5fH234AjOdnXvfuBfwzTQFi+6dN8WHh7fhFZswV3AcleCIkfwdS
qMLyPESilqmKV6hyp2UQIG5j2YAN4pfQmAvDII+sEy81NUo8xbzOHaCkLo1PE1J7
WnZirPyVpJwpSAarK75TcFPaJ/aLlwmsc9PwpSVovYusP169HPJHaqHcasPF1xVU
jiI+
-----END CERTIFICATE-----
)EOF";

// KEEP THIS VALUE PRIVATE AND SECURE!!!
const char CLIENT_KEY_PROG[] PROGMEM = R"KEY(
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCsnzpTjH0Yaw6M
aQsBIx6TJbEiwu12XEffMuIMwIkYupaaj5Zs3Wz3bhwoOVprn1kBoblDT71I0RQ6
aMHns3JUKgit274KO2X7w9uPhCygqPE74QBJr5PtZb0SRsyJrgKXmpeP99AfHxCZ
sG/nlARadAASP9ws03VZHQC/AaKVm+7kmIRfcEQ7UvdKQXzoATP/w6dEueD5rtvc
bshjEp8o5JIWc9DdO9+Tw/1iaStcyAjScA0zVpX2UMf9Yg9kmFYI99vu5MyOAMKt
6gajScFacdfEtJZmEfjpRUZrseZ6emq3tAAjqVE030aRBGhWZMbrmdSTL/JqXxom
RcAVFdTjAgMBAAECggEABSk+BqMEySNV1sw0w+liHhVFMRjDj65EpLvZSMyLGwby
6Y/jBkIDqbDai1Rx4NzC6JyUrcUVj9M6QpmyjgXnJGac4rTzjUvgO33MLKAzKH6L
tv0oodJ59BrFnEjV1rajusHFDvepesLyrY6PdmkqomBeKmZn8g3SsAkPLW3pa0zD
SKGHNyhb7ksI9Zlz+SvI7JEUbX642oPTpzxg6zsdZFu0PBBMAgbVpvcXNvhEFtbd
9P06d2NaOQyx9o0PdNIrJXc6uqxTicCUBAqmTeABOXyL5ydzrqe+ogmMbXqxNwVk
tMmji5GYS2bS0NlPS1h6jvUTUYD+4Nv27MJm0X6WeQKBgQDCkg8som635Gbuy8dF
ZFikf6ujf9QILWQ4To6YPlvyln5fO5DHz7MPCYcbOTDrzlSD42WJWlIyo5SnsY5f
k0lMixV4qEefsDv6BdPQQspekI9G5dird4Afm+UplBpTpHEH473TVPvapclPik4E
LI2S9sfLKeyTRslVi98fb9AXzwKBgQDjHzOOJNrv4bR9H+CDU1IdyiC9a1NQf/Yo
zuufFi2Vzl6Dtrb0Ir/NRVi/DVBpIfl51TTUVZBoYWhG1aionk2Lz7VysM9gAzEX
5O0Kr6F1NDwCgH+ZXR2mQuoPpJgbaqLVPRMfBLvLWctk1DUWfJX2o61RPHP3frnm
IQObY7/irQKBgGFDVFSSqlhA0/fBZE7a97jbnXhw+RRRZI0FMCEI4zvkYS3H//ry
Z+c3cxN3xm3KSdNYRDSiMv7faPtfNfWvEfAygrw7GvrHxWOZsCWmjbUx/H2LfoFQ
jnq+mpLrVzHCvUIdZZIUJIZLY9PgJlnNz8PMm1mDDqEcvJ6H+jSj11lfAoGBAId/
A8jXX+4gXwcOz2hJewHepm2a69don7h0ycjc+FEZDvXROZCocnjJ2EoSbVhrNmRi
t+O9MCu1gPpRWQ9Pcb/pKLzFktIa1V0F7Ayl/tLnWK29b2JVVOztmqm+bihdE8vX
ZeLpdge5CEic+RbzOJwtxaZjRGPwrIMISxiXB9D5AoGBALfleIc3C+N3oE/k1Y8P
VIzlhsWhhiD3Ye57eil3q29Ht1XWbECGPoXQwYNSnu+N3x7seGfqKHmxz9FrXfHP
dK7yfywrSKyO+OhI8uoXUMNWhFhddk7xtmyhoMmCJaYZ8eSorFe4YiBmzogONPby
ZIAOIjJz6MTKuHdsuJxdTUZZ
-----END PRIVATE KEY-----
)KEY";


#endif // SECRET