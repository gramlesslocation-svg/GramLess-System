import React from "react";
import { View, Text, FlatList } from "react-native";

export default function CartScreen({ route }) {
  const { cart } = route.params;

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 22, fontWeight: "bold" }}>
        Your Cart
      </Text>

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