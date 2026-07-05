import React, { useState } from "react";
import { View, Text, FlatList, Button } from "react-native";

// PRODUCTS
const products = [
  { id: "1", name: "Rice Golden", size: "800g", price: 5 },
  { id: "2", name: "Rice Golden", size: "2.4kg", price: 12 },
  { id: "3", name: "Rice Steam", size: "800g", price: 5 },
  { id: "4", name: "Rice Steam", size: "2.4kg", price: 12 },
  { id: "5", name: "Rice Creamy", size: "800g", price: 5 },
  { id: "6", name: "Rice Creamy", size: "2.4kg", price: 12 },
  { id: "7", name: "Rice White", size: "800g", price: 5 },
  { id: "8", name: "Rice White", size: "2.4kg", price: 12 },
];

export default function App() {
  const [screen, setScreen] = useState("home");
  const [cart, setCart] = useState([]);

  const addToCart = (item) => {
    setCart([...cart, item]);
  };

  // HOME SCREEN
  if (screen === "home") {
    return (
      <View style={{ flex: 1, padding: 20 }}>
        <Text style={{ fontSize: 22, fontWeight: "bold" }}>
          Grands Products
        </Text>

        <Button
          title={`Go to Cart (${cart.length})`}
          onPress={() => setScreen("cart")}
        />

        <FlatList
          data={products}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={{ padding: 10, borderWidth: 1, marginVertical: 5 }}>
              <Text>{item.name} - {item.size}</Text>
              <Text>${item.price}</Text>

              <Button
                title="Add"
                onPress={() => addToCart(item)}
              />
            </View>
          )}
        />
      </View>
    );
  }

  // CART SCREEN
  if (screen === "cart") {
    const total = cart.reduce((sum, item) => sum + item.price, 0);

    return (
      <View style={{ flex: 1, padding: 20 }}>
        <Text style={{ fontSize: 22, fontWeight: "bold" }}>
          Cart
        </Text>

        <Button title="Back" onPress={() => setScreen("home")} />

        <FlatList
          data={cart}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <Text>
              {item.name} - {item.size} - ${item.price}
            </Text>
          )}
        />

        <Text style={{ fontSize: 18, marginTop: 20 }}>
          Total: ${total}
        </Text>
      </View>
    );
  }
}