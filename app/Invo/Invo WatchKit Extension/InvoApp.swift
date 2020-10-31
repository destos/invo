//
//  InvoApp.swift
//  Invo WatchKit Extension
//
//  Created by Patrick Forringer on 10/31/20.
//

import SwiftUI

@main
struct InvoApp: App {
    @SceneBuilder var body: some Scene {
        WindowGroup {
            NavigationView {
                ContentView()
            }
        }

        WKNotificationScene(controller: NotificationController.self, category: "myCategory")
    }
}
