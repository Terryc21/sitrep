//
//  BadViewModel.swift
//  Fixture: a GENUINELY defective ViewModel — the known-positive case.
//
//  No @MainActor anywhere. A scan that reports zero findings against this fixture is
//  broken, and that is the whole point: the pre-2026-08-11 lookahead pattern returned
//  ZERO matches under the default Grep engine, which the grading rule then read as
//  "0-1 confirmed findings -> A". Silent, and biased toward a flattering grade.
//

import Foundation

@Observable
final class BadViewModel {

    var items: [String] = []

    // Capture list WITHOUT weak/unowned in a non-view class — a real retain-cycle risk.
    func load(completion: @escaping () -> Void) {
        Task { [self] in
            self.items = ["a", "b"]
            completion()
        }
    }
}
