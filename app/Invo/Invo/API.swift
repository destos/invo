// @generated
//  This file was automatically generated and should not be edited.

import Apollo
import Foundation

public enum SituationState: RawRepresentable, Equatable, Hashable, CaseIterable, Apollo.JSONDecodable, Apollo.JSONEncodable {
  public typealias RawValue = String
  case start
  case selecting
  case adding
  case placing
  case increment
  case consuming
  /// Auto generated constant for unknown enum values
  case __unknown(RawValue)

  public init?(rawValue: RawValue) {
    switch rawValue {
      case "START": self = .start
      case "SELECTING": self = .selecting
      case "ADDING": self = .adding
      case "PLACING": self = .placing
      case "INCREMENT": self = .increment
      case "CONSUMING": self = .consuming
      default: self = .__unknown(rawValue)
    }
  }

  public var rawValue: RawValue {
    switch self {
      case .start: return "START"
      case .selecting: return "SELECTING"
      case .adding: return "ADDING"
      case .placing: return "PLACING"
      case .increment: return "INCREMENT"
      case .consuming: return "CONSUMING"
      case .__unknown(let value): return value
    }
  }

  public static func == (lhs: SituationState, rhs: SituationState) -> Bool {
    switch (lhs, rhs) {
      case (.start, .start): return true
      case (.selecting, .selecting): return true
      case (.adding, .adding): return true
      case (.placing, .placing): return true
      case (.increment, .increment): return true
      case (.consuming, .consuming): return true
      case (.__unknown(let lhsValue), .__unknown(let rhsValue)): return lhsValue == rhsValue
      default: return false
    }
  }

  public static var allCases: [SituationState] {
    return [
      .start,
      .selecting,
      .adding,
      .placing,
      .increment,
      .consuming,
    ]
  }
}

public enum SituationExit: RawRepresentable, Equatable, Hashable, CaseIterable, Apollo.JSONDecodable, Apollo.JSONEncodable {
  public typealias RawValue = String
  case `open`
  case abandoned
  case completed
  /// Auto generated constant for unknown enum values
  case __unknown(RawValue)

  public init?(rawValue: RawValue) {
    switch rawValue {
      case "OPEN": self = .open
      case "ABANDONED": self = .abandoned
      case "COMPLETED": self = .completed
      default: self = .__unknown(rawValue)
    }
  }

  public var rawValue: RawValue {
    switch self {
      case .open: return "OPEN"
      case .abandoned: return "ABANDONED"
      case .completed: return "COMPLETED"
      case .__unknown(let value): return value
    }
  }

  public static func == (lhs: SituationExit, rhs: SituationExit) -> Bool {
    switch (lhs, rhs) {
      case (.open, .open): return true
      case (.abandoned, .abandoned): return true
      case (.completed, .completed): return true
      case (.__unknown(let lhsValue), .__unknown(let rhsValue)): return lhsValue == rhsValue
      default: return false
    }
  }

  public static var allCases: [SituationExit] {
    return [
      .open,
      .abandoned,
      .completed,
    ]
  }
}

public final class ActiveSituationQuery: GraphQLQuery {
  /// The raw GraphQL definition of this operation.
  public let operationDefinition: String =
    """
    query activeSituation {
      activeSituation {
        __typename
        state
        exitCondition
        items {
          __typename
          ... on Node {
            id
          }
          ... on Protocol {
            protocolUri
          }
          ... on ItemInterface {
            name
            data
          }
        }
      }
    }
    """

  public let operationName: String = "activeSituation"

  public init() {
  }

  public struct Data: GraphQLSelectionSet {
    public static let possibleTypes: [String] = ["Query"]

    public static var selections: [GraphQLSelection] {
      return [
        GraphQLField("activeSituation", type: .nonNull(.object(ActiveSituation.selections))),
      ]
    }

    public private(set) var resultMap: ResultMap

    public init(unsafeResultMap: ResultMap) {
      self.resultMap = unsafeResultMap
    }

    public init(activeSituation: ActiveSituation) {
      self.init(unsafeResultMap: ["__typename": "Query", "activeSituation": activeSituation.resultMap])
    }

    public var activeSituation: ActiveSituation {
      get {
        return ActiveSituation(unsafeResultMap: resultMap["activeSituation"]! as! ResultMap)
      }
      set {
        resultMap.updateValue(newValue.resultMap, forKey: "activeSituation")
      }
    }

    public struct ActiveSituation: GraphQLSelectionSet {
      public static let possibleTypes: [String] = ["Situation"]

      public static var selections: [GraphQLSelection] {
        return [
          GraphQLField("__typename", type: .nonNull(.scalar(String.self))),
          GraphQLField("state", type: .nonNull(.scalar(SituationState.self))),
          GraphQLField("exitCondition", type: .nonNull(.scalar(SituationExit.self))),
          GraphQLField("items", type: .nonNull(.list(.object(Item.selections)))),
        ]
      }

      public private(set) var resultMap: ResultMap

      public init(unsafeResultMap: ResultMap) {
        self.resultMap = unsafeResultMap
      }

      public init(state: SituationState, exitCondition: SituationExit, items: [Item?]) {
        self.init(unsafeResultMap: ["__typename": "Situation", "state": state, "exitCondition": exitCondition, "items": items.map { (value: Item?) -> ResultMap? in value.flatMap { (value: Item) -> ResultMap in value.resultMap } }])
      }

      public var __typename: String {
        get {
          return resultMap["__typename"]! as! String
        }
        set {
          resultMap.updateValue(newValue, forKey: "__typename")
        }
      }

      public var state: SituationState {
        get {
          return resultMap["state"]! as! SituationState
        }
        set {
          resultMap.updateValue(newValue, forKey: "state")
        }
      }

      public var exitCondition: SituationExit {
        get {
          return resultMap["exitCondition"]! as! SituationExit
        }
        set {
          resultMap.updateValue(newValue, forKey: "exitCondition")
        }
      }

      public var items: [Item?] {
        get {
          return (resultMap["items"] as! [ResultMap?]).map { (value: ResultMap?) -> Item? in value.flatMap { (value: ResultMap) -> Item in Item(unsafeResultMap: value) } }
        }
        set {
          resultMap.updateValue(newValue.map { (value: Item?) -> ResultMap? in value.flatMap { (value: Item) -> ResultMap in value.resultMap } }, forKey: "items")
        }
      }

      public struct Item: GraphQLSelectionSet {
        public static let possibleTypes: [String] = ["Item", "Tool", "Consumable", "TrackedConsumable"]

        public static var selections: [GraphQLSelection] {
          return [
            GraphQLField("__typename", type: .nonNull(.scalar(String.self))),
            GraphQLField("id", type: .nonNull(.scalar(GraphQLID.self))),
            GraphQLField("protocolUri", type: .scalar(String.self)),
            GraphQLField("name", type: .nonNull(.scalar(String.self))),
            GraphQLField("data", type: .scalar(String.self)),
          ]
        }

        public private(set) var resultMap: ResultMap

        public init(unsafeResultMap: ResultMap) {
          self.resultMap = unsafeResultMap
        }

        public static func makeItem(id: GraphQLID, protocolUri: String? = nil, name: String, data: String? = nil) -> Item {
          return Item(unsafeResultMap: ["__typename": "Item", "id": id, "protocolUri": protocolUri, "name": name, "data": data])
        }

        public static func makeTool(id: GraphQLID, protocolUri: String? = nil, name: String, data: String? = nil) -> Item {
          return Item(unsafeResultMap: ["__typename": "Tool", "id": id, "protocolUri": protocolUri, "name": name, "data": data])
        }

        public static func makeConsumable(id: GraphQLID, protocolUri: String? = nil, name: String, data: String? = nil) -> Item {
          return Item(unsafeResultMap: ["__typename": "Consumable", "id": id, "protocolUri": protocolUri, "name": name, "data": data])
        }

        public static func makeTrackedConsumable(id: GraphQLID, protocolUri: String? = nil, name: String, data: String? = nil) -> Item {
          return Item(unsafeResultMap: ["__typename": "TrackedConsumable", "id": id, "protocolUri": protocolUri, "name": name, "data": data])
        }

        public var __typename: String {
          get {
            return resultMap["__typename"]! as! String
          }
          set {
            resultMap.updateValue(newValue, forKey: "__typename")
          }
        }

        public var id: GraphQLID {
          get {
            return resultMap["id"]! as! GraphQLID
          }
          set {
            resultMap.updateValue(newValue, forKey: "id")
          }
        }

        public var protocolUri: String? {
          get {
            return resultMap["protocolUri"] as? String
          }
          set {
            resultMap.updateValue(newValue, forKey: "protocolUri")
          }
        }

        public var name: String {
          get {
            return resultMap["name"]! as! String
          }
          set {
            resultMap.updateValue(newValue, forKey: "name")
          }
        }

        public var data: String? {
          get {
            return resultMap["data"] as? String
          }
          set {
            resultMap.updateValue(newValue, forKey: "data")
          }
        }
      }
    }
  }
}
