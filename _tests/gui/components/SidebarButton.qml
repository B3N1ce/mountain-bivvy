// components/SidebarButton.qml
import QtQuick
import ".." // Zugriff auf Style.qml im Überordner

Rectangle {
    id: root
    property string label: "DEVICE"
    property bool active: false
    signal clicked()

    width: parent.width
    height: 60
    color: active ? "#2d2620" : "transparent"

    // Sanfter Farbübergang beim Aktivieren
    Behavior on color { ColorAnimation { duration: Style.animSpeed } }

    Rectangle {
        id: bar
        width: 4
        height: root.active ? parent.height : 0
        color: Style.orange
        anchors.left: parent.left
        // Animation: Balken wächst von der Mitte aus
        Behavior on height { NumberAnimation { duration: Style.animSpeed } }
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        text: root.label
        color: root.active ? "white" : Style.textGray
        anchors.centerIn: parent
        font.pixelSize: 12
        font.bold: true
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}