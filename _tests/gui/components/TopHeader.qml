import QtQuick
import QtQuick.Layouts
import ".." // Um auf Style.qml zuzugreifen

Rectangle {
    id: headerRoot
    implicitHeight: 60 // Die feste Höhe des Menüs
    Layout.fillWidth: true
    color: Style.bgSidebar // Gleiche Farbe wie Sidebar für nahtlosen Look
    
    // Eine feine Trennlinie nach unten (BaseCamp Style)
    Rectangle {
        anchors.bottom: parent.bottom
        width: parent.width
        height: 1
        color: "#2d2d2d"
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        spacing: 15

        Text {
            text: "BIVVY"
            color: Style.orange
            font.pixelSize: 18
            font.bold: true
            Layout.alignment: Qt.AlignVCenter
        }

        // Ein Spacer, der alles nachfolgende nach rechts schiebt (wie justify-content: space-between)
        Item { Layout.fillWidth: true }

        // Beispiel für ein Profil-Widget
        Row {
            spacing: 10
            Layout.alignment: Qt.AlignVCenter
            
            Text { 
                text: "Aktives Profil: **Standard**" 
                color: "white" 
                anchors.verticalCenter: parent.verticalCenter
            }
            
            Rectangle {
                width: 32; height: 32
                radius: 16
                color: "#444"
                // Hier käme später ein Image { source: "avatar.png" } rein
            }
        }
    }
}