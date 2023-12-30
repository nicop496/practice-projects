using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemigo : MonoBehaviour
{
    public float velocidad = 2f;
    private Rigidbody2D fisicas;

    // Start is called before the first frame update
    void Start()
    {
        fisicas = GetComponent<Rigidbody2D>();
        fisicas.velocity = Vector2.left * velocidad;
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.tag == "Destructor")
        {
            Destroy(gameObject);
        }
    }
}
