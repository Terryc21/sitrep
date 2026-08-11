//
//  GoodViewModel.swift
//  Fixture: a CORRECTLY annotated ViewModel.
//
//  The @MainActor sits THREE lines above the declaration, behind @available and
//  @Observable. Any scan that only inspects the declaration line — or only one line
//  above it — will wrongly report this file as a violation. That exact mistake was made
//  on 2026-08-11 against a real codebase and produced 5 false positives out of 5.
//

import Foundation
import SwiftUI

@available(iOS 17.0, macOS 14.0, *)
@MainActor
@Observable
final class GoodViewModel {

    var title: String = ""

    // A closure WITH a proper capture list — must not be flagged as a weak-self miss.
    func refresh(completion: @escaping () -> Void) {
        Task { [weak self] in
            guard let self else { return }
            self.title = "refreshed"
            completion()
        }
    }

    // try? where nil is the designed fallback — INTENTIONAL, not a finding.
    func cachedValue(from store: [String: String]) -> String {
        store["key"] ?? "default"
    }
}
