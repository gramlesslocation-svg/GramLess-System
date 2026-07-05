import React, { useState } from "react";
import { View, Text, FlatList, Button } from "react-native";
import { products } from "../data/products";

export default function HomeScreen({ navigation }) {
  const [cart, setCart] = useState([]);

  const addToCart = (item) => {
    setCart([...cart, item]);
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>

      <Text style={{ fontSize: 22, fontWeight: "bold" }}>
        Grands Rice Products
      </Text>

      <Button
        title={`Go to Cart (${cart.length})`}
        onPress={() => navigation.navigate("Cart", { cart })}
      />

      <FlatList
        data={products}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={{
            padding: 10,
            marginVertical: 5,
            borderWidth: 1,
            borderRadius: 8
          }}>
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