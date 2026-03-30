import QtQuick
import QtQuick.Controls

Window {
    width: 800
    height: 500
    
    visible: true
    title: "Bivvy QML Prototype"
    color: "#1e1e1e" // Dunkler Hintergrund wie BaseCamp

    // --- SIDEBAR ---
    Rectangle {
        id: sidebar
        width: 200
        height: parent.height
        color: "#252526"
        
        Column {
            anchors.fill: parent
            spacing: 2
            
            // Ein Custom-Button (wie ein Div mit Hover-Effekt)
            Rectangle {
                id: navButton
                width: parent.width
                height: 50
                color: mouseArea.containsMouse ? "#2e2e2e" : "transparent"
                
                // Der orange "Aktiv-Balken"
                Rectangle {
                    width: 4
                    height: parent.height
                    color: "#ff9800"
                    visible: true // Später an Zustand koppeln
                }

                Text {
                    text: "EVEREST CORE"
                    color: "white"
                    font.pixelSize: 12
                    font.bold: true
                    anchors.centerIn: parent
                }

                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: console.log("Everest ausgewählt!")
                }
            }
        }
    }

    // --- MAIN CONTENT AREA ---
    Rectangle {
        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        color: "#121212"

        Text {
            text: "Geräte-Einstellungen"
            color: "#888888"
            anchors.centerIn: parent
            font.pixelSize: 24
        }
        
        // Beispiel für ein QML Objekt: Ein schicker Schalter
        Switch {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 20
            text: "RGB Beleuchtung"
        }
    }
}