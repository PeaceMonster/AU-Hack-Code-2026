// ============================================================
//  F# Workshop: Exercises
//  Open in VS Code with Ionide. Run with: dotnet fsi exercises.fsx
//  Replace "failwith "TODO"" with your solutions.
//  Uncomment the printfn lines to test.
// ============================================================


// ── Shared types and data ───────────────────────────────

type DeliveryProfile =
    | Baseload                      // 24h
    | Peak of hours: int            // e.g. Peak 12 = 08:00–20:00

type Transaction =
    { Quantity: decimal   // MW
      Days: int
      Price: decimal      // EUR/MWh
      Profile: DeliveryProfile }

let transactions = [
    { Quantity = 50.0m; Days = 5; Price = 87.40m; Profile = Baseload }
    { Quantity = 25.0m; Days = 2; Price = 112.60m; Profile = Peak 12 }
    { Quantity = 30.0m; Days = 10; Price = 92.10m; Profile = Baseload }
    { Quantity = 40.0m; Days = 3; Price = 105.00m; Profile = Peak 12 }
]


// ── Exercise 1: Filtering Transactions ───────────────────
// Return only transactions with 5 or more days.

let longTransactions (transactions: Transaction list) : Transaction list =
    failwith "TODO"

// printfn "Ex 1: %A" (longTransactions transactions)
// Expected: two transactions (Days = 5 and Days = 10)


// ── Exercise 2: Describing Transactions ──────────────────
// Write a function that returns a human-readable string for a transaction.

let describe (t: Transaction) : string =
    failwith "TODO"

// printfn "Ex 2a: %s" (describe transactions.[0])
// printfn "Ex 2b: %s" (describe transactions.[1])
// printfn "Ex 2c: %s" (describe transactions.[2])
// printfn "Ex 2d: %s" (describe transactions.[3])
// Expected:
// "50 MW Baseload for 5 days @ 87.40 EUR/MWh"
// "25 MW Peak 12 for 2 days @ 112.60 EUR/MWh"
// "30 MW Baseload for 10 days @ 92.10 EUR/MWh"
// "40 MW Peak 12 for 3 days @ 105.00 EUR/MWh"


// ── Exercise 3: Contract Value ───────────────────────────
// Calculate the total EUR value of a contract.
// Baseload = 24h/day, Peak = the number of hours it carries.
// Value = Quantity × Days × Hours per day × Price
// Hint: convert an int to decimal with the `decimal` function, e.g. decimal 24

let contractValue (transaction: Transaction) : decimal =
    failwith "TODO"

// printfn "Ex 3a: %M" (contractValue transactions.[0])
// printfn "Ex 3b: %M" (contractValue transactions.[1])
// printfn "Ex 3c: %M" (contractValue transactions.[2])
// printfn "Ex 3d: %M" (contractValue transactions.[3])
// Expected: 524400, 67560, 663120, 151200


// ── Exercise 4: Value per Delivery Profile ──────────────
// Group transactions by DeliveryProfile and calculate total value per profile.
// Reuse your contractValue function from Exercise 3.

let valuePerProfile (transactions: Transaction list) =
    transactions
    |> id  // replace with your pipeline

// printfn "Ex 4: %A" (valuePerProfile transactions)
// Expected (order may vary):
// [(Baseload, 1187520); (Peak 12, 218760)]
