// Main.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"
import "."

Window {
    width: 900
    height: 600
    visible: true
    title: "Bivvy QML"
    color: Style.bgDark
    
    minimumWidth: 800
    minimumHeight: 600

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // SIDEBAR
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.25
            color: Style.bgSidebar

            Layout.minimumWidth: 200
            Layout.maximumWidth: 350

            Column {
                anchors.fill: parent
                anchors.topMargin: 20
                spacing: 5

                // Wir nutzen einen Repeater für die Buttons
                Repeater {
                    model: ["EVEREST", "DISPLAYPAD", "MAKROS"]
                    delegate: SidebarButton {
                        label: modelData
                        active: mainStack.currentIndex === index
                        onClicked: mainStack.currentIndex = index
                    }
                }
            }
        }

        // CONTENT AREA
        StackLayout {
            id: mainStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: 0

            // Page 1: Everest
            Rectangle { 
                color: "transparent"
                Column {
                    anchors.centerIn: parent
                    spacing: 20
                    Text { text: "Everest Configuration"; color: "white"; font.pixelSize: 30 }
                    // DATEN VON PYTHON
                    Text { 
                        text: "System Temp: " + python.cpu_temp + "°C"
                        color: python.cpu_temp > 50 ? "red" : Style.orange
                        font.pixelSize: 18
                    }
                }
            }

            // Page 2: DisplayPad
            Rectangle { 
                color: "transparent"
                Text { text: "DisplayPad Settings"; color: "white"; anchors.centerIn: parent; font.pixelSize: 30 }
            }
        }
    }
}