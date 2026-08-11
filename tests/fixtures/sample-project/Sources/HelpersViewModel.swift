//
//  HelpersViewModel.swift
//  Fixture: a file NAMED *ViewModel.swift that contains NO ViewModel.
//
//  Two enum namespaces of static helpers. There is no class, no struct, no observable
//  state — so the absence of @MainActor is CORRECT, not a finding.
//
//  This is the filename-is-not-a-type trap. On 2026-08-11 a reviewer built "ground
//  truth" by globbing *ViewModel.swift and testing for @MainActor, and this shape made
//  the baseline wrong before any scan ran. Grade on the TYPES a pattern returns, never
//  on a filename inventory.
//

import Foundation

enum PriceFormatting {
    static func format(_ cents: Int) -> String {
        let dollars = Decimal(cents) / 100
        return dollars.formatted(.currency(code: "USD"))
    }
}

enum SlotLimits {
    static let maxPhotos = 5

    static func remaining(current: Int) -> Int {
        max(0, maxPhotos - current)
    }
}
