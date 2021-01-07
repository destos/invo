//
//  Network.swift
//  Invo
//
//  Created by Patrick Forringer on 11/1/20.
//

import Foundation
import Apollo

class Network {
  static let shared = Network()
    
  private(set) lazy var apollo = ApolloClient(url: URL(string: "http://localhost:8000/graphql")!)
}
