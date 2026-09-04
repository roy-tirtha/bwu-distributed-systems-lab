# 🖥️ Java RMI Calculator — Client-Server Project

## 🤔 What even is this?

Okay so normally when you write a Java program, everything runs on **one machine, one JVM**. You call a method, it runs right there in memory.

But what if the method you want to call lives on a **completely different computer** (or a different process)? That's the exact problem **RMI (Remote Method Invocation)** solves. It lets a Java program on one machine call a method on an object that's sitting on *another* machine — and it *feels* like a normal local method call, even though under the hood there's a whole network conversation happening.

This project is a tiny working demo of that: a **Calculator** whose `add()` and `multiply()` methods live on a **Server**, and a **Client** that calls those methods remotely and gets the answer back — like ordering food through a waiter instead of walking into the kitchen yourself. 🍽️

---

## 🧩 Why does it need so many files?

RMI isn't just "client talks to server." It has a specific 4-part structure, and every file here plays one specific role in that structure:

```
📁 RMI-Calculator/
│
├── 📜 Calculator.java        → The "contract" (interface)
├── ⚙️  CalculatorImpl.java    → The actual logic (implementation)
├── 🖥️  Server.java            → Hosts the object, makes it reachable
├── 🙋 Client.java            → Calls the remote methods
│
└── 🧱 .class files            → Compiled bytecode for each of the above
```

### 📜 `Calculator.java` — the contract
This is just an **interface** that extends `Remote`. It doesn't do any math — it just says *"any class that implements me must offer an `add()` and a `multiply()` method, and both must be able to throw a `RemoteException`"*.

Think of it like a job posting: it lists what the job requires, not who's doing it.

Why `RemoteException`? Because unlike a normal method call, a remote call can fail for reasons that have nothing to do with your logic — network drops, server crashes, timeouts. Java forces you to acknowledge that possibility.

### ⚙️ `CalculatorImpl.java` — the actual worker
This class **implements** `Calculator` and does the real math (`a + b`, `a * b`). It also extends `UnicastRemoteObject`, which is the part that quietly does all the heavy lifting: it makes this object capable of receiving calls *from the network*, not just from inside the same JVM. The moment you call `super()` in the constructor, this object basically becomes "network-reachable."

### 🖥️ `Server.java` — the host
The server's job is simple:
1. Create a `CalculatorImpl` object (the real worker).
2. Start an **RMI Registry** on port `1099` — think of this as a phonebook 📖 that maps names to remote objects.
3. `rebind()` the calculator into that phonebook under the name `"CalculatorService"`.

After this, the server just sits there and waits. It doesn't loop or poll — RMI's networking magic handles incoming calls in the background.

### 🙋 `Client.java` — the requester
The client:
1. Looks up the **same registry** (`localhost:1099`) the server created.
2. Asks it: *"give me whatever is registered as `CalculatorService`"*.
3. Casts that thing to a `Calculator` reference.
4. Calls `.add()` and `.multiply()` on it — **exactly like calling a local method** — except this call actually travels over the network to the server, runs there, and the result travels back.

That last point is the entire magic trick of RMI: the client code has *no idea* the object is remote. It just sees an interface and calls methods on it.

---

## 🔄 How a single request actually flows

```
        1️⃣ Server starts
        ┌──────────────────────┐
        │   Server.java        │
        │  creates             │
        │  CalculatorImpl      │
        └─────────┬────────────┘
                  │ registers as "CalculatorService"
                  ▼
        ┌─────────────────────┐
        │   RMI Registry        │   📖 (port 1099, acts like a phonebook)
        └─────────┬───────────┘
                  ▲
                  │ 2️⃣ looks up "CalculatorService"
        ┌─────────┴────────────┐
        │   Client.java          │
        │  gets Calculator ref   │
        └─────────┬────────────┘
                  │ 3️⃣ calculator.add(a, b)
                  ▼
        ┌─────────────────────┐
        │  Travels over network │  🌐
        │  to CalculatorImpl    │
        └─────────┬───────────┘
                  │ 4️⃣ computes result
                  ▼
        ┌─────────────────────┐
        │  Result sent back      │  ↩️
        │  to Client             │
        └─────────────────────┘
```

---

## ▶️ Running order matters

Since the client *looks up* something the server *registers*, there's only one order that works:

1. **Start `Server.java` first** — it needs to create the registry and bind the object before anyone can look it up.
2. **Then run `Client.java`** — it connects to the already-running registry and grabs the remote reference.

If you run the client before the server, `registry.lookup("CalculatorService")` will fail because there's nothing registered yet. 🚫

---

## 🧠 The one-line mental model

> **Interface = promise, Impl = worker, Registry = phonebook, Server = the one who lists the number, Client = the one who dials it.**

That's genuinely the whole idea — everything else in RMI is just Java's plumbing to make a network call *look* like a normal function call.
