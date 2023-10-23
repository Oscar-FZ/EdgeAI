LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI += " \
    file://facedetection.py \
    file://model.tflite \
    file://cascade_frontalface_default.xml \
"

S = "${WORKDIR}"

TARGET_CC_ARCH += "${LDFLAGS}"

do_install () {
    	install -d ${D}${bindir}
    	install -m 0755 facedetection.py ${D}${bindir}
    	install -m 0755 model.tflite ${D}${bindir}
    	install -m 0755 cascade_frontalface_default.xml ${D}${bindir}
}

