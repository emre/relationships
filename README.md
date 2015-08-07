relationships
---
redis backed user relationships on it's simplest form.

####installation

```bash
$ [sudo] pip install relationships
```
or if you like 90s:
```bash
$ [sudo] easy_install relationships
```

####usage

**getting the Relationship class**

```python
from relationships import Relationship
r = Relationship()
```

**follow**

```python

r('Guido').follow('Rasmus')
r('Guido').follow('Larry')
r('Larry').follow('Guido')
r('Rasmus').follow('Guido')
r('Dave').follow('Guido')
r('Larry').follow('Guido')

```

**unfollow**

```python
r('Guido').unfollow("Rasmus")
```

**block**
```python
r('Guido').block("Guido")
r('Rasmus').block("Guido")
```

**unblock**
```python
r('Rasmus').unblock('Guido')
```

**getting friends**
```python
r('Guido').friends()
```

```bash
>>> {'Larry', 'Rasmus'}
```

**getting mutual friends**

```python
r('Guido').mutual_friends('Rasmus')
```

**getting followers**

```python
r("Guido").followers()
```

```bash
>>> {'Dave', 'Larry', 'Rasmus'}
```
**getting followings**

```python
r("Guido").following()
```

```bash
>>> {'Larry', 'Rasmus'}
```
**getting a simple graph of spesific user**
```python

r('Zlatan Ibrahimovic').follow("Galatasaray")
r('Galatasaray').follow("Zlatan Ibrahimovic")
r('Galatasaray').follow("Podolski")
r('Galatasaray').follow("Drogba")
r('Galatasaray').follow("Sneijder")
r('Galatasaray').follow("Zlatan Ibrahimovic")
r('Sneijder').follow("Galatasaray")
r('Podolski').follow("Galatasaray")

r("Galatasaray").get_network("/tmp/galatasaray_network.png")
```
*(you need graphviz (system library) and pydot (pylibrary) installed to get this functionality.*
<img src="http://i.imgur.com/HakrxvJ.png">


**getting block list by user**

```python
# people blocked by guido
r('Guido').blocks()
```

```bash
>>> {'Rasmus'}
```

**getting blocked list by user**

```python
# people who blocked Guido
r('Guido').blocked()
```

```bash
>>> {'Rasmus'}
```

**counts**
```python
r('Guido').block_count() # count of people blocked by Guido
r('Guido').blocked_count() # count of people who blocked Guido

r('Guido').follower_count() # count of people who follows Guido
r('Guido').following_count() # count of people following by Guido
```

**checks**

```python
r('Guido').is_following('Rasmus') # does Guido follows Rasmus?
r('Rasmus').is_follower('Guido') # is Rasmus a follower of Guido?

r('Guido').is_blocked('Rasmus') # did Guido blocked Rasmus?
r('Rasmus').is_blocked_by('Guido') # is Rasmus blocked by Guido?
```

